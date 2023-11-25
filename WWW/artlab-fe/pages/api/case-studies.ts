import { supabase } from "lib/supabase"
import { NextApiRequest, NextApiResponse } from 'next'

export default async (req: NextApiRequest, res: NextApiResponse) => {
    switch (req.method) {
        case 'GET':
            return getCaseStudies(req, res);
        case 'POST':
            return postCaseStudies(req, res);
        default:
            res.setHeader('Allow', ['GET', 'POST', 'PUT', 'DELETE']);
            return res.status(405).end(`Method ${req.method} Not Allowed`);
    }
};

const getCaseStudies = async (req: NextApiRequest, res: NextApiResponse) => {
    try {
        const data = await supabase
            .from('case_studies')
            .select('*');
        res.status(200).json(data);
    } catch (error) {
        console.error('Error fetching posts:', error);
        res.status(500).json({ error: 'Internal server error' });
    }
}

const postCaseStudies = async (_: NextApiRequest, res: NextApiResponse) => {
    const { formData } = _.body;
    try {
        const data = await supabase
            .from('case_studies')
            .insert(formData);
        res.status(200).json(data);
    } catch (error) {
        console.error('Error fetching posts:', error);
        res.status(500).json({ error: 'Internal server error' });
    }
}

