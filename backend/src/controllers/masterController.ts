// controllers/masterController.ts

import { Request, Response } from 'express';
import * as fs from 'fs';
import { config } from '../app';
import fetch from 'node-fetch';


const loadMasterDocumentFile = (fileUri: string): Promise<any> => {
    const filePath = fileUri.slice(7);
    return new Promise((resolve, reject) => {
        fs.readFile(filePath, 'utf8', (err, data) => {
            if (err) {
                console.error('Error reading master document:', err);
                return reject(new Error('Error reading master document'));
            }
            resolve(JSON.parse(data));
        });
    });
};

const loadMasterDocumentURI = async (uri: string): Promise<any> => {
    //const fetch = (await import('node-fetch')).default; // Dynamic import
    const response = await fetch(uri);
    if (!response.ok) {
        throw new Error('Error fetching master document from URI');
    }
    return response.json();
};

const processMasterDocument = async (data: any) => {
    let masterDocument = {};
    masterDocument.version = data.version;
    masterDocument.name = data.name;
    masterDocument.description = data.description;
    // loop through data_objects and add them to masterDocument
    masterDocument.data_objects = [];
    for (let dataObject of data.data_objects) {
        masterDocument.data_objects.push({
            id: dataObject.id,
            name: dataObject.name,
            description: dataObject.description
        });
    }
    return masterDocument;
};

export const getMasterDocument = async (req: Request, res: Response) => {
    if (!config.masterDocumentUri) {
        throw new Error('masterDocumentUri is not defined in the configuration.');
    }

    try {
        let data;
        if (config.masterDocumentUri.startsWith('file:///')) {
            data = await loadMasterDocumentFile(config.masterDocumentUri);
        } else {
            data = await loadMasterDocumentURI(config.masterDocumentUri);
        }
        data = await processMasterDocument(data);
        res.json(data);
    } catch (error: unknown) {
        if (error instanceof Error) {
            res.status(500).json({ message: error.message });
        } else {
            res.status(500).json({ message: 'An unknown error occurred' });
        }
    }
}; 