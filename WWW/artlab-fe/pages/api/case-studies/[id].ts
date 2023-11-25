import { supabase } from "lib/supabase";
import { NextApiRequest, NextApiResponse } from "next";

export default async (req: NextApiRequest, res: NextApiResponse) => {
  switch (req.method) {
    case "GET":
      return getCaseStudies(req, res);
    case "PUT":
      return updateCaseStudy(req, res);
    case "DELETE":
      return deleteCaseStudy(req, res);
    default:
      res.setHeader("Allow", ["GET", "POST", "PUT", "DELETE"]);
      return res.status(405).end(`Method ${req.method} Not Allowed`);
  }
};

const getCaseStudies = async (req: NextApiRequest, res: NextApiResponse) => {
  const {
    query: { id },
  } = req;
  try {
    const data = await supabase
      .from("case_studies")
      .select("*")
      .eq("id", id)
      .single();
    res.status(200).json(data);
  } catch (error) {
    console.error("Error fetching posts:", error);
    res.status(500).json({ error: "Internal server error" });
  }
};

const updateCaseStudy = async (_: NextApiRequest, res: NextApiResponse) => {
  const { formData } = _.body;
  const {
    query: { id },
  } = _;
  try {
    const data = await supabase
      .from("case_studies")
      .update(formData)
      .match({ id: id });
    res.status(200).json(data);
  } catch (error) {
    console.error("Error fetching posts:", error);
    res.status(500).json({ error: "Internal server error" });
  }
};

const deleteCaseStudy = async (_: NextApiRequest, res: NextApiResponse) => {
  const {
    query: { id },
  } = _;
  try {
    const data = await supabase.from("case_studies").delete().match({ id: id });
    res.status(200).json(data);
  } catch (error) {
    console.error("Error fetching posts:", error);
    res.status(500).json({ error: "Internal server error" });
  }
};
