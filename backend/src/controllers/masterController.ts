import { Request, Response } from 'express';
import * as fs from 'fs';
import * as path from 'path';

export const getMasterDocument = (req: Request, res: Response) => {
    const filePath = path.join(__dirname, '../../data/master.json');

    fs.readFile(filePath, 'utf8', (err, data) => {
        if (err) {
            return res.status(500).json({ message: 'Error reading master document' });
        }
        res.json(JSON.parse(data));
    });
}; 