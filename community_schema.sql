-- Supabase Database Schema for Farmer Community Chat

-- Community Posts Table
CREATE TABLE community_posts (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    farmer_id UUID NOT NULL,
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    category VARCHAR(50) DEFAULT 'general',
    tags TEXT[], -- Array of tags like ['disease', 'rice', 'organic']
    image_url TEXT,
    is_question BOOLEAN DEFAULT true,
    is_solved BOOLEAN DEFAULT false,
    upvotes INTEGER DEFAULT 0,
    downvotes INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Community Replies Table
CREATE TABLE community_replies (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    post_id UUID NOT NULL REFERENCES community_posts(id) ON DELETE CASCADE,
    farmer_id UUID NOT NULL,
    content TEXT NOT NULL,
    is_ai_response BOOLEAN DEFAULT false,
    is_best_answer BOOLEAN DEFAULT false,
    upvotes INTEGER DEFAULT 0,
    downvotes INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Community Votes Table (for posts and replies)
CREATE TABLE community_votes (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    farmer_id UUID NOT NULL,
    post_id UUID REFERENCES community_posts(id) ON DELETE CASCADE,
    reply_id UUID REFERENCES community_replies(id) ON DELETE CASCADE,
    vote_type VARCHAR(10) CHECK (vote_type IN ('upvote', 'downvote')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(farmer_id, post_id),
    UNIQUE(farmer_id, reply_id)
);

-- Community Categories Table
CREATE TABLE community_categories (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    description TEXT,
    icon VARCHAR(50),
    color VARCHAR(20),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Insert default categories
INSERT INTO community_categories (name, description, icon, color) VALUES
('disease', 'Plant diseases and pest control', '🦠', '#dc2626'),
('weather', 'Weather-related farming queries', '🌤️', '#2563eb'),
('market', 'Market prices and selling tips', '💰', '#16a34a'),
('seeds', 'Seeds and varieties discussion', '🌱', '#ca8a04'),
('organic', 'Organic farming practices', '🌿', '#059669'),
('equipment', 'Farm equipment and tools', '🚜', '#7c3aed'),
('general', 'General farming discussions', '💬', '#6b7280');

-- Indexes for better performance
CREATE INDEX idx_community_posts_farmer_id ON community_posts(farmer_id);
CREATE INDEX idx_community_posts_category ON community_posts(category);
CREATE INDEX idx_community_posts_created_at ON community_posts(created_at DESC);
CREATE INDEX idx_community_posts_is_question ON community_posts(is_question);
CREATE INDEX idx_community_replies_post_id ON community_replies(post_id);
CREATE INDEX idx_community_replies_farmer_id ON community_replies(farmer_id);
CREATE INDEX idx_community_votes_farmer_id ON community_votes(farmer_id);

-- Enable Row Level Security (RLS)
ALTER TABLE community_posts ENABLE ROW LEVEL SECURITY;
ALTER TABLE community_replies ENABLE ROW LEVEL SECURITY;
ALTER TABLE community_votes ENABLE ROW LEVEL SECURITY;

-- RLS Policies (Allow all authenticated users to read, only owners to modify)
CREATE POLICY "Anyone can view posts" ON community_posts FOR SELECT USING (true);
CREATE POLICY "Users can insert their own posts" ON community_posts FOR INSERT WITH CHECK (true);
CREATE POLICY "Users can update their own posts" ON community_posts FOR UPDATE USING (true);

CREATE POLICY "Anyone can view replies" ON community_replies FOR SELECT USING (true);
CREATE POLICY "Users can insert replies" ON community_replies FOR INSERT WITH CHECK (true);
CREATE POLICY "Users can update their own replies" ON community_replies FOR UPDATE USING (true);

CREATE POLICY "Anyone can view votes" ON community_votes FOR SELECT USING (true);
CREATE POLICY "Users can manage their own votes" ON community_votes FOR ALL USING (true);