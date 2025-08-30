-- Krishi Sahayak Database Schema for Supabase PostgreSQL
-- Run this in Supabase SQL Editor

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Farmers table (linked to Clerk user_id)
CREATE TABLE farmers (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    clerk_user_id VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    phone VARCHAR(15),
    email VARCHAR(255),
    place VARCHAR(255) NOT NULL,
    district VARCHAR(255),
    state VARCHAR(255),
    pincode VARCHAR(10),
    farm_size_acres DECIMAL(10,2),
    farming_experience_years INTEGER,
    preferred_language VARCHAR(10) DEFAULT 'en',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Crops table
CREATE TABLE crops (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    farmer_id UUID REFERENCES farmers(id) ON DELETE CASCADE,
    crop_name VARCHAR(255) NOT NULL,
    variety VARCHAR(255),
    area_acres DECIMAL(10,2),
    planting_date DATE,
    expected_harvest_date DATE,
    season VARCHAR(50), -- kharif, rabi, zaid
    irrigation_type VARCHAR(100),
    farming_method VARCHAR(100), -- organic, conventional, mixed
    status VARCHAR(50) DEFAULT 'active', -- active, harvested, failed
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Insured crops table
CREATE TABLE insured_crops (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    farmer_id UUID REFERENCES farmers(id) ON DELETE CASCADE,
    crop_id UUID REFERENCES crops(id) ON DELETE CASCADE,
    insurance_company VARCHAR(255) NOT NULL,
    policy_number VARCHAR(255) UNIQUE NOT NULL,
    coverage_amount DECIMAL(12,2) NOT NULL,
    premium_amount DECIMAL(10,2) NOT NULL,
    policy_start_date DATE NOT NULL,
    policy_end_date DATE NOT NULL,
    coverage_type VARCHAR(100), -- weather, yield, revenue
    status VARCHAR(50) DEFAULT 'active', -- active, claimed, expired
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- NFT certificates table
CREATE TABLE nft_certificates (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    farmer_id UUID REFERENCES farmers(id) ON DELETE CASCADE,
    crop_id UUID REFERENCES crops(id) ON DELETE CASCADE,
    token_id VARCHAR(255) UNIQUE,
    contract_address VARCHAR(255),
    blockchain_network VARCHAR(50) DEFAULT 'polygon',
    certificate_type VARCHAR(100), -- organic, quality, harvest
    metadata_ipfs_hash VARCHAR(255),
    transaction_hash VARCHAR(255),
    minted_at TIMESTAMP WITH TIME ZONE,
    certificate_data JSONB, -- flexible data storage
    status VARCHAR(50) DEFAULT 'pending', -- pending, minted, transferred
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Plant disease scans table
CREATE TABLE plant_scans (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    farmer_id UUID REFERENCES farmers(id) ON DELETE CASCADE,
    crop_id UUID REFERENCES crops(id) ON DELETE SET NULL,
    image_url VARCHAR(500),
    disease_detected VARCHAR(255),
    confidence_score DECIMAL(5,4),
    treatment_recommendation TEXT,
    scan_date TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    weather_conditions JSONB,
    ai_model_version VARCHAR(50)
);

-- Create indexes for better performance
CREATE INDEX idx_farmers_clerk_user_id ON farmers(clerk_user_id);
CREATE INDEX idx_crops_farmer_id ON crops(farmer_id);
CREATE INDEX idx_insured_crops_farmer_id ON insured_crops(farmer_id);
CREATE INDEX idx_nft_certificates_farmer_id ON nft_certificates(farmer_id);
CREATE INDEX idx_plant_scans_farmer_id ON plant_scans(farmer_id);

-- Create updated_at trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Add triggers for updated_at
CREATE TRIGGER update_farmers_updated_at BEFORE UPDATE ON farmers FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_crops_updated_at BEFORE UPDATE ON crops FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_insured_crops_updated_at BEFORE UPDATE ON insured_crops FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_nft_certificates_updated_at BEFORE UPDATE ON nft_certificates FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();