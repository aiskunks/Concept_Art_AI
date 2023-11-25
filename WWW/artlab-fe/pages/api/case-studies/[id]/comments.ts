import { NextApiRequest, NextApiResponse } from 'next';
import { supabase } from 'lib/supabase';

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  const caseStudyId = req.query.id as string;

  if (req.method === 'GET') {
    const { data, error } = await supabase
      .from('comments')
      .select('*')
      .eq('case_study_id', caseStudyId);

    if (error) {
      return res.status(500).json({ error: 'Error fetching comments' });
    }

    return res.status(200).json({ comments: data });
  }

  if (req.method === 'POST') {
    const { content } = req.body;

    console.log("POST COMMENT")

    if (!content) {
      return res.status(400).json({ error: 'Content is required' });
    }

    const { data, error } = await supabase
      .from('comments')
      .insert([{ content, case_study_id: caseStudyId }]);

    if (error) {
      return res.status(500).json({ error });
    }

    return res.status(201).json({ comment: data });
  }

  return res.status(405).end(); // Method not allowed
}
