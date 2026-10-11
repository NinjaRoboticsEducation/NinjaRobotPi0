/**
 * @file App.jsx
 * @description Root application component with React Router configuration.
 * 
 * Routes:
 * - "/" (Home): Landing page with quick actions and power-off slider
 * - "/agent": AI chat and browser voice input
 * - "/movement": Direct native controls
 * - "/help": Legacy redirect to Home
 */
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Layout from './components/layout/Layout';
import Home from './pages/Home';
import Agent from './pages/Agent';
import Movement from './pages/Movement';

function App() {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<Layout />}>
                    <Route index element={<Home />} />
                    <Route path="agent" element={<Agent />} />
                    <Route path="movement" element={<Movement />} />
                    <Route path="help" element={<Navigate to="/" replace />} />
                    <Route path="*" element={<Navigate to="/" replace />} />
                </Route>
            </Routes>
        </BrowserRouter>
    );
}

export default App;
