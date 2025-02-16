// app.ts

import express from 'express';
import bodyParser from 'body-parser';
import cors from 'cors';
import masterRoutes from './routes/masterRoutes';
import dotenv from 'dotenv';

// Load environment variables from .env file
dotenv.config();

// Configuration object
const config = {
    dataObjectTypeBaseUri: String(process.env.DATA_OBJECT_TYPE_BASE_URI),
    masterDocumentUri: String(process.env.MASTER_DOCUMENT_URI),
};

// Validation function
const validateConfig = () => {
    if (!config.dataObjectTypeBaseUri) {
        throw new Error('Missing required environment variable: DATA_OBJECT_TYPE_BASE_URI');
    }
    if (!config.masterDocumentUri) {
        throw new Error('Missing required environment variable: MASTER_DOCUMENT_URI');
    }
};

// Validate the configuration
validateConfig();

export { config };

const app = express();
const PORT = process.env.PORT || 1081;

app.use(cors());
app.use(bodyParser.json());
app.use('/api/', masterRoutes);


app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
}); 