// controllers/masterController.ts

import { Request, Response } from 'express';
import * as fs from 'fs';
import * as path from 'path';
import { config } from '../app'; // Import the config from app.ts

export const getMasterDocument = (req: Request, res: Response) => {
    if (!config.masterDocumentUri) {
        throw new Error('masterDocumentUri is not defined in the configuration.');
    }

    // if filePath begins with file:/// then remove the file:// part
    if (config.masterDocumentUri.startsWith('file://')) {
        const filePath = config.masterDocumentUri.slice(7);

        fs.readFile(filePath, 'utf8', (err, data) => {
            if (err) {
                console.error('Error reading master document:', err);
                return res.status(500).json({ message: 'Error reading master document' });
            }
            res.json(JSON.parse(data));
        });
    }
}; 