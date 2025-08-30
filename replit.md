# Krishi Sahayak - The Farmer's AI Co-pilot

## Overview

Krishi Sahayak is a comprehensive Progressive Web App (PWA) designed to serve as an AI-powered farming assistant for Indian farmers. The application provides plant disease detection using AI, real-time weather forecasting, market price information, and blockchain-based digital crop passports. Built with accessibility and simplicity in mind, it features a clean interface with large text and intuitive navigation to serve farmers with varying levels of technical literacy.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Framework**: Flask-based web application with Jinja2 templating
- **UI Framework**: Bootstrap 5 with custom CSS for responsive design
- **PWA Implementation**: Service worker, web manifest, and offline capabilities
- **Design System**: Nature-inspired color palette (greens, browns, blues) with large typography using Poppins font
- **Responsive Design**: Mobile-first approach with card-based layouts optimized for farming environments

### Backend Architecture
- **Framework**: Flask (Python) with modular service architecture
- **Database ORM**: SQLAlchemy with declarative base for data modeling
- **Session Management**: Flask sessions with configurable secret keys
- **File Handling**: Werkzeug for secure file uploads with size limits (16MB)
- **Middleware**: ProxyFix for handling reverse proxy headers

### Data Models
- **User**: Stores farmer profiles with phone authentication, location (PIN code), and crop preferences
- **ScanResult**: Records AI diagnosis results, treatment recommendations, and weather warnings
- **DigitalPassport**: Blockchain-verified crop certificates with NFT token IDs and IPFS hashes

### Service Layer Architecture
- **AI Service**: Integrates with Groq API for plant pathology analysis using base64 image encoding
- **Weather Service**: AccuWeather API integration with location-based forecasting and rain warnings
- **Market Service**: Market price aggregation with trend analysis and crop-specific pricing

### Authentication System
- **OTP-based Authentication**: Phone number-based registration and login
- **Session Management**: Server-side session storage with user state persistence
- **Profile Completion**: Progressive onboarding with mandatory farmer profile setup

## External Dependencies

### Third-Party APIs
- **Groq API**: AI-powered plant disease detection and treatment recommendations
- **AccuWeather API**: Weather forecasting and location services using PIN code lookup
- **AGMARKNET**: Market price data aggregation for crop pricing information

### Blockchain Infrastructure
- **Polygon Mumbai Testnet**: NFT minting for digital crop passports
- **MetaMask Integration**: Wallet connectivity for blockchain interactions
- **IPFS via Pinata**: Decentralized storage for NFT metadata and crop documentation

### Frontend Libraries
- **Bootstrap 5**: UI component framework and responsive grid system
- **Heroicons**: SVG icon library for consistent visual elements
- **Poppins Font**: Google Fonts integration for accessibility and readability

### Development Tools
- **Werkzeug**: WSGI utilities and development server
- **PIL (Pillow)**: Image processing for uploaded plant photos
- **SQLAlchemy**: Database abstraction and ORM functionality

### Infrastructure Services
- **File Storage**: Local file system for image uploads with configurable paths
- **Database**: SQLite for development with PostgreSQL compatibility for production
- **PWA Capabilities**: Service worker for offline functionality and app-like experience