import express from 'express';
import bodyParser from 'body-parser';
import cors from 'cors';
import masterRoutes from './routes/masterRoutes';

const app = express();
const PORT = process.env.PORT || 1081;

app.use(cors());
app.use(bodyParser.json());
app.use('/api/master', masterRoutes);

app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
}); 