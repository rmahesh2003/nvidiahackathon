# DocuSynth AI Frontend

A modern React/Next.js frontend for DocuSynth AI, providing an intuitive interface for uploading codebases and viewing analysis results.

## 🎨 Features

- **Drag & Drop Upload**: Easy file upload with visual feedback
- **Real-time Progress**: Live updates on analysis progress and agent status
- **Beautiful Results Display**: Structured presentation of analysis results
- **Responsive Design**: Works on desktop and mobile devices
- **Modern UI**: Built with Tailwind CSS and Lucide React icons

## 🚀 Quick Start

### Prerequisites
- Node.js 16+
- npm or yarn

### Installation

1. **Install dependencies:**
```bash
npm install
```

2. **Start the development server:**
```bash
npm run dev
```

3. **Open your browser:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000 (must be running)

## 🏗️ Project Structure

```
frontend/
├── src/
│   ├── pages/
│   │   ├── index.tsx          # Main application page
│   │   └── _app.tsx           # App wrapper
│   └── styles/
│       └── globals.css        # Global styles and Tailwind
├── public/                    # Static assets
├── package.json
├── tailwind.config.js         # Tailwind configuration
├── next.config.js            # Next.js configuration
└── tsconfig.json             # TypeScript configuration
```

## 🎯 Usage

### Uploading a Codebase

1. **Prepare your codebase:**
   - Create a zip file containing your code files
   - Supported file types: `.js`, `.jsx`, `.ts`, `.tsx`, `.py`

2. **Upload:**
   - Drag and drop the zip file onto the upload area
   - Or click to browse and select the file

3. **Monitor Progress:**
   - Watch real-time progress updates
   - See agent status (Internal Doc, Library Doc, Context Manager)

4. **View Results:**
   - Project summary with statistics
   - File-by-file analysis
   - Function documentation
   - External library information
   - Cross-references between files

## 🎨 UI Components

### Upload Area
- Drag and drop interface
- Visual feedback for active states
- File type validation

### Progress Display
- Animated progress bar
- Agent status indicators
- Real-time updates

### Results Display
- **Project Summary**: Overview with statistics
- **File Analysis**: Individual file breakdowns
- **Functions**: Documentation for each function
- **Libraries**: External dependency information
- **Cross References**: Function usage across files

## 🔧 Configuration

### Environment Variables

Create a `.env.local` file:

```env
# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000

# Development
NODE_ENV=development
```

### Tailwind CSS

The project uses Tailwind CSS for styling. Configuration is in `tailwind.config.js`:

```javascript
module.exports = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: { /* custom colors */ },
        secondary: { /* custom colors */ }
      }
    }
  }
}
```

## 🧪 Testing

### Manual Testing

1. **Start both servers:**
```bash
# Terminal 1 - Backend
cd backend && uvicorn app.main:app --reload

# Terminal 2 - Frontend
cd frontend && npm run dev
```

2. **Test with sample data:**
   - Create a zip file from the `sample_data/` directory
   - Upload through the web interface
   - Verify results display correctly

### Automated Testing

```bash
# Run tests
npm test

# Run tests with coverage
npm test -- --coverage
```

## 🚀 Production Build

### Build for Production

```bash
npm run build
npm start
```

### Docker Deployment

1. Create a Dockerfile:
```dockerfile
FROM node:16-alpine

WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

COPY . .
RUN npm run build

EXPOSE 3000
CMD ["npm", "start"]
```

2. Build and run:
```bash
docker build -t docusynth-frontend .
docker run -p 3000:3000 docusynth-frontend
```

## 🎨 Customization

### Styling

The UI is built with Tailwind CSS. To customize:

1. **Colors**: Modify `tailwind.config.js`
2. **Components**: Edit component files in `src/pages/`
3. **Global Styles**: Update `src/styles/globals.css`

### Adding New Features

1. **New Pages**: Add files to `src/pages/`
2. **Components**: Create reusable components in `src/components/`
3. **API Integration**: Update API calls in components

## 🔍 Performance

### Optimization

- **Code Splitting**: Next.js automatic code splitting
- **Image Optimization**: Built-in Next.js image optimization
- **Bundle Analysis**: Use `npm run build` to see bundle size

### Monitoring

- **Performance**: Use browser DevTools
- **Errors**: Check browser console and network tab
- **Analytics**: Add Google Analytics or similar

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details. 