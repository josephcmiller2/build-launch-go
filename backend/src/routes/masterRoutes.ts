import { Router } from 'express';
import { getMasterDocument } from '../controllers/masterController';

const router = Router();

router.get('/', getMasterDocument);

export default router; 