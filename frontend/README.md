# SAFEHER Frontend

A modern React + TypeScript frontend for the SAFEHER women safety application.

## 🚀 Quick Start

### Prerequisites
- Node.js 16+ 
- npm or yarn

### Installation

```bash
cd frontend
npm install
```

### Development

```bash
npm run dev
```

The app will run on `http://localhost:3000`

### Build for Production

```bash
npm run build
```

## 📋 Features

- **User Authentication** - Login/Register with username and PIN
- **Safety Check** - Real-time location analysis with risk assessment
- **Emergency Contacts** - Manage and view emergency contacts
- **SOS Alert** - One-click emergency alert system
- **Location History** - Track location history with timestamps
- **Responsive Design** - Works on desktop and mobile devices

## 🏗️ Project Structure

```
frontend/
├── src/
│   ├── components/        # Reusable React components
│   ├── pages/            # Page components (Login, Dashboard)
│   ├── services/         # API service layer
│   ├── styles/           # CSS styles
│   ├── App.tsx           # Main app component
│   └── main.tsx          # Entry point
├── public/               # Static assets
├── package.json          # Dependencies
├── tsconfig.json         # TypeScript config
├── vite.config.ts        # Vite config
├── tailwind.config.js    # Tailwind CSS config
└── .env.example          # Environment variables template
```

## 🔌 API Configuration

Create a `.env` file in the frontend directory:

```env
VITE_API_URL=http://localhost:5000
VITE_APP_NAME=SAFEHER
```

Make sure your backend is running on `http://localhost:5000`

## 🎨 Tech Stack

- **React 18** - UI framework
- **TypeScript** - Type safety
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **Axios** - HTTP client
- **Lucide React** - Icons

## 📱 Mobile Support

The app is fully responsive and works on:
- Desktop browsers (Chrome, Firefox, Safari, Edge)
- Mobile browsers (iOS Safari, Chrome Android)

For native mobile app, use React Native (coming soon).

## 🔐 Security Notes

- Username is stored in localStorage for session persistence
- Use HTTPS in production
- Keep backend API URL secure
- Implement JWT tokens in production

## 📖 API Endpoints Used

- `GET /ping` - Health check
- `POST /register` - User registration
- `GET /user/<username>` - Get user info
- `POST /contact` - Add emergency contact
- `GET /contacts/<username>` - Get contacts
- `POST /analyze` - Analyze location safety
- `GET /locations/<username>` - Get location history
- `POST /sos` - Trigger SOS alert

## 🛠️ Development

### Available Scripts

```bash
npm run dev        # Start development server
npm run build      # Build for production
npm run preview    # Preview production build
npm run lint       # Run ESLint
```

### Browser DevTools

Install React Developer Tools extension for better debugging.

## 📝 License

Proprietary - SAFEHER Team

## 🤝 Support

For issues or questions, contact the development team.
