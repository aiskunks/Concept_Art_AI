import { NextApiRequest, NextApiResponse } from "next";
import { supabase } from "lib/supabase";

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse,
) {
  const caseStudyId = req.query.id as string;
  const commentId = req.query.commId;

  if (req.method === "PUT") {
    const { content } = req.body;

    if (!content) {
      return res.status(400).json({ error: "Content is required" });
    }

    const { data, error } = await supabase
      .from("comments")
      .update({ content })
      .eq("id", commentId)
      .eq("case_study_id", caseStudyId);

    if (error) {
      return res.status(500).json({ error });
    }

    return res.status(200).json(data);
  }

  if (req.method === "DELETE") {
    const { data, error } = await supabase
      .from("comments")
      .delete()
      .eq("id", commentId)
      .eq("case_study_id", caseStudyId);

    if (error) {
      return res.status(500).json({ error: "Error deleting comment" });
    }

    return res.status(204).end();
  }

  return res.status(405).end();
}
