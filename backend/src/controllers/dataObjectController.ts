import { Request, Response } from 'express';
import * as fs from 'fs';
import fetch from 'node-fetch';
import { config } from '../app';

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

export const getDataObject = async (req: Request, res: Response) => {
    const { id } = req.params; // Assuming the data object ID is passed as a URL parameter

    // TODO: Implement the logic to get the data object
}; 