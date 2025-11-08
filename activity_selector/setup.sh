#!/usr/bin/env bash
# Activity Selector - Cross-Platform Setup Script
# This Bash script works on Ubuntu/Linux

set -e

echo "========================================"
echo "   Activity Selector - Setup Wizard"
echo "========================================"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Check Python installation
echo -e "${YELLOW}🐍 Checking Python installation...${NC}"
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo -e "${GREEN}✅ Python found: $PYTHON_VERSION${NC}"
else
    echo -e "${RED}❌ Python 3 is not installed!${NC}"
    echo ""
    echo -e "${YELLOW}Please install Python 3.8 or higher:${NC}"
    echo "  sudo apt-get update"
    echo "  sudo apt-get install python3 python3-pip python3-tk"
    echo ""
    exit 1
fi

echo ""

# Check if tkinter is available
echo -e "${YELLOW}🖼️  Checking tkinter...${NC}"
if python3 -c "import tkinter" &> /dev/null; then
    echo -e "${GREEN}✅ tkinter is available${NC}"
else
    echo -e "${YELLOW}⚠️  tkinter is not installed!${NC}"
    echo ""
    read -p "Would you like to install tkinter now? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${CYAN}📥 Installing tkinter...${NC}"
        sudo apt-get update
        sudo apt-get install -y python3-tk
        echo -e "${GREEN}✅ tkinter installed successfully!${NC}"
    else
        echo -e "${YELLOW}Warning: The application requires tkinter to run!${NC}"
    fi
fi

echo ""

# Check if Poetry is installed
echo -e "${YELLOW}📦 Checking Poetry installation...${NC}"
if command -v poetry &> /dev/null; then
    POETRY_VERSION=$(poetry --version)
    echo -e "${GREEN}✅ Poetry found: $POETRY_VERSION${NC}"
else
    echo -e "${YELLOW}⚠️  Poetry is not installed!${NC}"
    echo ""
    read -p "Would you like to install Poetry now? (y/n) " -n 1 -r
    echo ""
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${CYAN}📥 Installing Poetry...${NC}"
        curl -sSL https://install.python-poetry.org | python3 -
        
        # Add Poetry to PATH for this session
        export PATH="$HOME/.local/bin:$PATH"
        
        # Check if installation was successful
        if command -v poetry &> /dev/null; then
            echo -e "${GREEN}✅ Poetry installed successfully!${NC}"
            echo ""
            echo -e "${YELLOW}⚠️  Please add Poetry to your PATH:${NC}"
            echo "  export PATH=\"\$HOME/.local/bin:\$PATH\""
            echo ""
            echo "Add this line to your ~/.bashrc or ~/.zshrc to make it permanent."
            echo ""
        else
            echo -e "${RED}❌ Failed to install Poetry automatically.${NC}"
            echo "Please install manually: https://python-poetry.org/docs/#installation"
            exit 1
        fi
    else
        echo ""
        echo -e "${YELLOW}Poetry is required to continue. Install it manually:${NC}"
        echo "  curl -sSL https://install.python-poetry.org | python3 -"
        exit 1
    fi
fi

echo ""

# Navigate to project directory
cd "$(dirname "$0")"

# Install dependencies
echo -e "${CYAN}📦 Installing project dependencies...${NC}"
poetry install

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Dependencies installed successfully!${NC}"
else
    echo -e "${RED}❌ Failed to install dependencies!${NC}"
    exit 1
fi

echo ""

# Check for data files
echo -e "${YELLOW}📄 Checking data files...${NC}"

if [ ! -f "activities_data.yml" ]; then
    if [ -f "activities_data_example.yml" ]; then
        echo -e "${YELLOW}⚠️  activities_data.yml not found. Creating from example...${NC}"
        cp "activities_data_example.yml" "activities_data.yml"
        echo -e "${GREEN}✅ Created activities_data.yml${NC}"
    else
        echo -e "${YELLOW}⚠️  No activity data found. You'll need to add activities manually.${NC}"
    fi
else
    echo -e "${GREEN}✅ activities_data.yml found${NC}"
fi

if [ ! -f "config.yml" ]; then
    echo -e "${CYAN}ℹ️  config.yml will be created on first run${NC}"
else
    echo -e "${GREEN}✅ config.yml found${NC}"
fi

echo ""

# Check image cache directory
if [ ! -d "image_cache" ]; then
    echo -e "${YELLOW}📁 Creating image_cache directory...${NC}"
    mkdir -p "image_cache"
    echo -e "${GREEN}✅ image_cache directory created${NC}"
else
    echo -e "${GREEN}✅ image_cache directory exists${NC}"
fi

# Make launcher scripts executable
echo ""
echo -e "${YELLOW}🔧 Setting execute permissions on launcher scripts...${NC}"
chmod +x start.sh run.py
echo -e "${GREEN}✅ Permissions set${NC}"

echo ""
echo "========================================"
echo -e "${GREEN}   ✅ Setup Complete!${NC}"
echo "========================================"
echo ""
echo -e "${CYAN}To run the application:${NC}"
echo "  ./start.sh"
echo ""
echo -e "${CYAN}Or manually:${NC}"
echo "  poetry run python run.py"
echo ""

# Ask if user wants to run now
read -p "Would you like to run the application now? (y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo -e "${GREEN}🚀 Launching Activity Selector...${NC}"
    echo ""
    poetry run python run.py
fi
