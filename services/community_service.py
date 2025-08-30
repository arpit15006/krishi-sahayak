#!/usr/bin/env python3
import os
import requests
from datetime import datetime, timedelta
from supabase import create_client, Client

class CommunityService:
    def __init__(self):
        self.supabase_url = os.getenv('SUPABASE_URL', 'https://your-project.supabase.co')
        self.supabase_key = os.getenv('SUPABASE_ANON_KEY', 'your-anon-key')
        self.supabase: Client = create_client(self.supabase_url, self.supabase_key)
        self.groq_api_key = os.getenv('GROQ_API_KEY')

    def get_posts(self, category=None, limit=20, offset=0):
        """Get community posts with pagination"""
        try:
            query = self.supabase.table('community_posts').select('*')
            
            if category and category != 'all':
                query = query.eq('category', category)
            
            result = query.order('created_at', desc=True).range(offset, offset + limit - 1).execute()
            
            return {
                'success': True,
                'posts': result.data,
                'count': len(result.data)
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def create_post(self, farmer_id, title, content, category='general', tags=None, is_question=True):
        """Create a new community post"""
        try:
            post_data = {
                'farmer_id': farmer_id,
                'title': title,
                'content': content,
                'category': category,
                'tags': tags or [],
                'is_question': is_question,
                'created_at': datetime.now().isoformat()
            }
            
            result = self.supabase.table('community_posts').insert(post_data).execute()
            
            # Generate AI response if it's a question
            if is_question and result.data:
                post_id = result.data[0]['id']
                self._generate_ai_response(post_id, title, content, category)
            
            return {
                'success': True,
                'post': result.data[0] if result.data else None
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def get_post_details(self, post_id):
        """Get post with replies"""
        try:
            # Get post
            post_result = self.supabase.table('community_posts').select('*').eq('id', post_id).execute()
            if not post_result.data:
                return {'success': False, 'error': 'Post not found'}
            
            # Get replies
            replies_result = self.supabase.table('community_replies').select('*').eq('post_id', post_id).order('created_at').execute()
            
            return {
                'success': True,
                'post': post_result.data[0],
                'replies': replies_result.data
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def create_reply(self, post_id, farmer_id, content, is_ai_response=False):
        """Create a reply to a post"""
        try:
            reply_data = {
                'post_id': post_id,
                'farmer_id': farmer_id,
                'content': content,
                'is_ai_response': is_ai_response,
                'created_at': datetime.now().isoformat()
            }
            
            result = self.supabase.table('community_replies').insert(reply_data).execute()
            
            return {
                'success': True,
                'reply': result.data[0] if result.data else None
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def vote_post(self, farmer_id, post_id, vote_type):
        """Vote on a post (upvote/downvote)"""
        try:
            # Check if user already voted
            existing_vote = self.supabase.table('community_votes').select('*').eq('farmer_id', farmer_id).eq('post_id', post_id).execute()
            
            if existing_vote.data:
                # Update existing vote
                self.supabase.table('community_votes').update({'vote_type': vote_type}).eq('id', existing_vote.data[0]['id']).execute()
            else:
                # Create new vote
                vote_data = {
                    'farmer_id': farmer_id,
                    'post_id': post_id,
                    'vote_type': vote_type
                }
                self.supabase.table('community_votes').insert(vote_data).execute()
            
            # Update post vote counts
            self._update_post_votes(post_id)
            
            return {'success': True}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def vote_reply(self, farmer_id, reply_id, vote_type):
        """Vote on a reply"""
        try:
            # Check if user already voted
            existing_vote = self.supabase.table('community_votes').select('*').eq('farmer_id', farmer_id).eq('reply_id', reply_id).execute()
            
            if existing_vote.data:
                # Update existing vote
                self.supabase.table('community_votes').update({'vote_type': vote_type}).eq('id', existing_vote.data[0]['id']).execute()
            else:
                # Create new vote
                vote_data = {
                    'farmer_id': farmer_id,
                    'reply_id': reply_id,
                    'vote_type': vote_type
                }
                self.supabase.table('community_votes').insert(vote_data).execute()
            
            # Update reply vote counts
            self._update_reply_votes(reply_id)
            
            return {'success': True}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def get_categories(self):
        """Get all community categories"""
        try:
            result = self.supabase.table('community_categories').select('*').order('name').execute()
            return {
                'success': True,
                'categories': result.data
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def search_posts(self, query, category=None):
        """Search posts by title and content"""
        try:
            # Simple text search (Supabase full-text search would be better)
            search_query = self.supabase.table('community_posts').select('*')
            
            if category and category != 'all':
                search_query = search_query.eq('category', category)
            
            # Use ilike for case-insensitive search
            search_query = search_query.or_(f'title.ilike.%{query}%,content.ilike.%{query}%')
            
            result = search_query.order('created_at', desc=True).execute()
            
            return {
                'success': True,
                'posts': result.data
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def _generate_ai_response(self, post_id, title, content, category):
        """Generate AI response for a question"""
        try:
            # Create farming expert prompt
            prompt = f"""आप एक कृषि विशेषज्ञ हैं। एक किसान ने यह सवाल पूछा है:

शीर्षक: {title}
सवाल: {content}
श्रेणी: {category}

कृपया हिंदी में व्यावहारिक और उपयोगी सलाह दें। 3-4 वाक्यों में जवाब दें।"""
            
            url = "https://api.groq.com/openai/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {self.groq_api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": "llama-3.2-90b-text-preview",
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 200,
                "temperature": 0.8
            }
            
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                ai_response = result['choices'][0]['message']['content']
                
                # Create AI reply
                self.create_reply(post_id, 'ai-moderator', ai_response, is_ai_response=True)
            
        except Exception as e:
            print(f"AI response generation failed: {e}")

    def _update_post_votes(self, post_id):
        """Update post vote counts"""
        try:
            # Count upvotes and downvotes
            upvotes = self.supabase.table('community_votes').select('*').eq('post_id', post_id).eq('vote_type', 'upvote').execute()
            downvotes = self.supabase.table('community_votes').select('*').eq('post_id', post_id).eq('vote_type', 'downvote').execute()
            
            # Update post
            self.supabase.table('community_posts').update({
                'upvotes': len(upvotes.data),
                'downvotes': len(downvotes.data)
            }).eq('id', post_id).execute()
            
        except Exception as e:
            print(f"Vote update failed: {e}")

    def _update_reply_votes(self, reply_id):
        """Update reply vote counts"""
        try:
            # Count upvotes and downvotes
            upvotes = self.supabase.table('community_votes').select('*').eq('reply_id', reply_id).eq('vote_type', 'upvote').execute()
            downvotes = self.supabase.table('community_votes').select('*').eq('reply_id', reply_id).eq('vote_type', 'downvote').execute()
            
            # Update reply
            self.supabase.table('community_replies').update({
                'upvotes': len(upvotes.data),
                'downvotes': len(downvotes.data)
            }).eq('id', reply_id).execute()
            
        except Exception as e:
            print(f"Vote update failed: {e}")

    def get_farmer_info(self, farmer_id):
        """Get farmer information for display"""
        try:
            if farmer_id == 'ai-moderator':
                return {
                    'name': 'AI कृषि सलाहकार',
                    'place': 'डिजिटल असिस्टेंट',
                    'is_ai': True
                }
            
            # Get from farmers table (assuming it exists)
            result = self.supabase.table('farmers').select('name, place').eq('id', farmer_id).execute()
            if result.data:
                return {
                    'name': result.data[0]['name'],
                    'place': result.data[0]['place'],
                    'is_ai': False
                }
            else:
                return {
                    'name': 'अज्ञात किसान',
                    'place': 'अज्ञात स्थान',
                    'is_ai': False
                }
        except Exception as e:
            return {
                'name': 'अज्ञात किसान',
                'place': 'अज्ञात स्थान',
                'is_ai': False
            }

# Global instance
community_service = CommunityService()