import { Request, Response } from 'express';
import * as fs from 'fs';
import fetch from 'node-fetch';
import { config } from '../app';
import { loadMasterDocument } from './masterController';

const loadDataObjectFile = (fileUri: string): Promise<any> => {
    const filePath = fileUri.slice(7);
    return new Promise((resolve, reject) => {
        fs.readFile(filePath, 'utf8', (err, data) => {
            if (err) {
                console.error('Error reading data object file:', err);
                return reject(new Error('Error reading data object file'));
            }
            resolve(JSON.parse(data));
        });
    });
};

const loadDataObjectURI = async (uri: string): Promise<any> => {
    const response = await fetch(uri);
    if (!response.ok) {
        throw new Error('Error fetching data object from URI');
    }
    return response.json();
};

export const loadDataObject = async (uri: string): Promise<any> => {
    if (uri.startsWith('file:///')) {
        return await loadDataObjectFile(uri);
    } else if (/^[A-Za-z0-9_-]+:\//.test(uri)) {
        return await loadDataObjectURI(uri);
    } else {
        // we need to preprend with dataObjectTypeBaseUri
        let fullUri = `${config.dataObjectTypeBaseUri}/${uri}`;

        if (fullUri.startsWith('file:///')) {
            return await loadDataObjectFile(fullUri);
        } else {
            return await loadDataObjectURI(fullUri);
        }
    }
};

const getDataObjectPathFromMasterDocument = (masterDocument: any, dataObjectId: string): string => {
    // loop through masterDocument.data_objects and return the path of the data object that matches the id
    for (let dataObject of masterDocument.data_objects) {
        if (dataObject.id === dataObjectId) {
            return dataObject.uri;
        }
    }
};

export const getDataObject = async (req: Request, res: Response) => {
    // Get the id from the request parameters
    const id = req.params.id;

    try {
        // Load the master document
        let masterDocument = await loadMasterDocument(config.masterDocumentUri);
        
        // Get the data object path from the master document using the id
        let dataObjectPath = getDataObjectPathFromMasterDocument(masterDocument, id);
        
        // Load the data object using the path
        let dataObject = await loadDataObject(dataObjectPath);
        
        // Send the data object as a response
        res.json(dataObject);
    } catch (error: unknown) {
        if (error instanceof Error) {
            res.status(500).json({ message: error.message });
        } else {
            res.status(500).json({ message: 'An unknown error occurred' });
        }
    }
}; 