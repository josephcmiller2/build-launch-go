import { Router } from 'express';
import { getMasterDocument } from '../controllers/masterController';
import { getDataObject } from '../controllers/dataObjectController';
const router = Router();

router.get('/master', getMasterDocument);
router.get('/object/:id', getDataObject);

export default router; 