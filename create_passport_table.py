"""
Create digital_passports table in Supabase
"""

from config.database import supabase_admin

def create_passport_table():
    try:
        # Create the table using SQL
        sql = """
        CREATE TABLE IF NOT EXISTS digital_passports (
            id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
            farmer_id UUID REFERENCES farmers(id) ON DELETE CASCADE,
            crop_type VARCHAR(100) NOT NULL,
            season VARCHAR(50) NOT NULL,
            nft_token_id VARCHAR(100),
            ipfs_hash VARCHAR(100),
            verified BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        );
        
        -- Create index for faster queries
        CREATE INDEX IF NOT EXISTS idx_digital_passports_farmer_id ON digital_passports(farmer_id);
        CREATE INDEX IF NOT EXISTS idx_digital_passports_token_id ON digital_passports(nft_token_id);
        """
        
        result = supabase_admin.rpc('exec_sql', {'sql': sql}).execute()
        print("✅ Digital passports table created successfully")
        return True
        
    except Exception as e:
        print(f"❌ Error creating table: {e}")
        
        # Try alternative approach - insert a test record to create table structure
        try:
            test_data = {
                'farmer_id': '6a126e29-bc4a-4ac8-b352-793924a94db7',  # Your existing farmer ID
                'crop_type': 'Test Crop',
                'season': 'Test Season',
                'nft_token_id': 'TEST-001',
                'ipfs_hash': 'QmTest123',
                'verified': False
            }
            
            result = supabase_admin.table('digital_passports').insert(test_data).execute()
            print("✅ Digital passports table created via insert")
            
            # Delete test record
            supabase_admin.table('digital_passports').delete().eq('nft_token_id', 'TEST-001').execute()
            print("✅ Test record cleaned up")
            
            return True
            
        except Exception as e2:
            print(f"❌ Alternative approach failed: {e2}")
            return False

if __name__ == "__main__":
    print("🗄️ Creating digital_passports table...")
    create_passport_table()