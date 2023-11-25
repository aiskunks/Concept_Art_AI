import React, { useEffect, useState } from "react";
import { useUser } from "@supabase/auth-helpers-react";

interface CaseStudy {
  id: number;
  title: string;
  description: string;
  content: string;
  author: string;
  comments: Comment[];
  user_id: string;
  // an other required fields...
}

interface Comment {
  id: number;
  content: string;
  author: string;
  user_id: string;
  case_study_id: number;
}

export default function Page() {
  const user = useUser();
  const [caseStudies, setCaseStudies] = useState<CaseStudy[]>([]);
  const [currentCaseStudy, setCurrentCaseStudy] = useState<CaseStudy>();
  const [isUpdate, setIsUpdate] = useState<boolean>(false);
  const [showForm, setShowForm] = useState(false);
  const [comments, setComments] = useState<Comment[]>([]);
  const [newComment, setNewComment] = useState("");
  const [currCommentId, setCurrentCommentId] = useState<number>();
  const [editComment, setEditComment] = useState(false);
  const [formData, setFormData] = useState({
    title: "",
    description: "",
    content: "",
    author: "",
    user_id: user?.id,
  });
  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>,
  ) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const createNew = () => {
    setIsUpdate(false);
    setFormData({
      title: "",
      description: "",
      content: "",
      author: "",
      user_id: user?.id,
    });
    toggleForm();
  };

  const toggleForm = () => {
    setShowForm(!showForm);
  };
  const fetchCaseStudyById = async (id: any) => {
    try {
      const response = await fetch(`/api/case-studies/${id}`);
      const data = await response.json();
      setFormData(data.data);
      setCurrentCaseStudy(data.data);
    } catch (error) {
      console.error("Error fetching case studies:", error);
    } finally {
    }
  };

  const fetchCaseStudies = async () => {
    try {
      const response = await fetch("/api/case-studies");
      const data = await response.json();
      setCaseStudies(data.data);
    } catch (error) {
      console.error("Error fetching case studies:", error);
    }
  };

  const handleSubmitForm = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!isUpdate) {
      try {
        const response = await fetch("/api/case-studies", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ formData: formData }),
        });
        const data = await response.json();
        fetchCaseStudies();
        toggleForm();
      } catch (error) {
        console.error("Error fetching case studies:", error);
      } finally {
      }
    } else {
      setUpdatedCaseStudy();
    }
  };

  const updateCaseStudy = (id: any) => {
    toggleForm();
    setIsUpdate(!isUpdate);
    fetchCaseStudyById(id);
  };

  const setUpdatedCaseStudy = async () => {

    try {
      const response = await fetch(
        `/api/case-studies/${currentCaseStudy?.id}`,
        {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            formData: formData,
            currentCaseStudy: currentCaseStudy,
          }),
        },
      );
      const data = await response.json();
      fetchCaseStudies();
      setIsUpdate(false);
      toggleForm();
    } catch (error) {
      console.error("Error fetching case studies:", error);
    }
  };

  const deleteCaseStudy = async (id: any) => {
    try {
      const response = await fetch(
        `/api/case-studies/${id}`,
        {
          method: "DELETE",
          headers: {
            "Content-Type": "application/json",
          },
        },
      );
      const data = await response.json();
      fetchCaseStudies();
    } catch (error) {
      console.error("Error fetching case studies:", error);
    }
  };

  const fetchCommentsForCaseStudy = async (caseStudyId: number) => {
    console.log("23802833209802");
    try {
      const response = await fetch(`/api/case-studies/${caseStudyId}/comments`);
      const data = await response.json();
      const comments = data.comments;
      setComments(comments);
    } catch (error) {
      console.error("Error fetching comments:", error);
    }
  };

  const handleCaseStudyClick = (caseStudy: CaseStudy) => {
    setCurrentCaseStudy(caseStudy);
    fetchCommentsForCaseStudy(caseStudy.id);
  };

  const handleNewCommentChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>,
  ) => {
    setNewComment(e.target.value);
  };

  const handleAddComment = async (caseStudyId: number) => {
    try {
      const response = await fetch(
        `/api/case-studies/${caseStudyId}/comments`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ content: newComment }),
        },
      );
      const data = await response.json();
      setNewComment("");
      fetchCommentsForCaseStudy(currentCaseStudy?.id || 0); // Refetch comments
    } catch (error) {
      console.error("Error adding comment:", error);
    }
  };

  const handleEditComment = async (commentId: number, content: string) => {
    setEditComment(true);
    setCurrentCommentId(commentId);
    setNewComment(content);
  };

  const submitUpdatedComment = async (
    caseStudyId: number,
    commentId: number,
  ) => {
    try {
      const response = await fetch(
        `/api/case-studies/${caseStudyId}/comments/${commentId}`,
        {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ content: newComment }),
        },
      );
      const data = await response.json();
      setNewComment(""); 
      setEditComment(false);
      fetchCommentsForCaseStudy(caseStudyId);
    } catch (error) {
      console.error("Error adding comment:", error);
    }
  };

  const handleDeleteComment = async (
    caseStudyId: number,
    commentId: number,
  ) => {
    try {
      const response = await fetch(
        `/api/case-studies/${caseStudyId}/comments/${commentId}`,
        {
          method: "DELETE",
          headers: {
            "Content-Type": "application/json",
          },
        },
      );
      fetchCommentsForCaseStudy(caseStudyId);
    } catch (error) {
      console.error("Error adding comment:", error);
    }
  };

  useEffect(() => {
    if (user) fetchCaseStudies();
  }, [user]);

  return (
    <div className="relative overflow-x-auto">
      <div>
        <button
          className="m-4 bg-transparent font-semibold hover:text-white py-2 px-4 border border-white-500 hover:border-blue-500 rounded"
          onClick={() => createNew()}
        >{`Create a new Case Study`}</button>
      </div>
      {showForm && (
        <form
          onSubmit={handleSubmitForm}
          className="p-4 m-4 border border-gray-600 rounded-lg max-w-sm mx-auto"
        >
          <div className="mb-5">
            <div className="flex justify-end" onClick={toggleForm}>
              X
            </div>
            <label
              htmlFor="title"
              className="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
            >
              Title:
            </label>
            <input
              type="text"
              id="title"
              name="title"
              value={formData.title}
              onChange={handleChange}
              className="block w-full p-2 text-gray-900 border border-gray-300 rounded-lg bg-gray-50 sm:text-xs focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
            />
          </div>
          <div className="mb-5">
            <label
              htmlFor="description"
              className="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
            >
              Description:
            </label>
            <input
              type="text"
              id="description"
              name="description"
              value={formData.description}
              onChange={handleChange}
              className="block w-full p-2 text-gray-900 border border-gray-300 rounded-lg bg-gray-50 sm:text-xs focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
            />
          </div>
          <div className="mb-5">
            <label
              htmlFor="content"
              className="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
            >
              Content:
            </label>
            <textarea
              id="content"
              name="content"
              value={formData.content}
              onChange={handleChange}
              className="block w-full p-2 text-gray-900 border border-gray-300 rounded-lg bg-gray-50 sm:text-xs focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
            />
          </div>
          <div className="mb-5">
            <label
              htmlFor="author"
              className="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
            >
              Author:
            </label>
            <input
              type="text"
              id="author"
              name="author"
              value={formData.author}
              onChange={handleChange}
              className="block w-full p-2 text-gray-900 border border-gray-300 rounded-lg bg-gray-50 sm:text-xs focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
            />
          </div>
          <div className="mb-5 flex justify-center">
            <button
              className=" bg-cyan-700 hover:bg-cyan-800 text-white font-bold py-2 px-4 rounded-full"
              type="submit"
            >
              Submit
            </button>
          </div>
        </form>
      )}
      <table className="w-full text-sm text-left rtl:text-right text-gray-500 dark:text-gray-400">
        <thead className="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
          <tr>
            <th scope="col" className="px-6 py-3">
              ID
            </th>
            <th scope="col" className="px-6 py-3">
              Title
            </th>
            <th scope="col" className="px-6 py-3">
              Description
            </th>
            <th scope="col" className="px-6 py-3">
              Content
            </th>
            <th scope="col" className="px-6 py-3">
              Author
            </th>
            <th scope="col" className="px-6 py-3">
              Actions
            </th>
          </tr>
        </thead>
        <tbody>
          {caseStudies.map((study) => (
            <React.Fragment key={study.id}>
              <tr
                onClick={() => handleCaseStudyClick(study)}
                key={study.id}
                className="bg-white border-b dark:bg-gray-800 dark:border-gray-700"
                style={{ cursor: "pointer" }}
              >
                <th
                  scope="row"
                  className="px-6 py-4 font-medium text-gray-900 whitespace-nowrap dark:text-white"
                >
                  {study.id}
                </th>
                <td
                  className="px-6 py-4"
                  onClick={() => fetchCommentsForCaseStudy(study.id)}
                >
                  {" "}
                  {study.title}
                </td>
                <td className="px-6 py-4"> {study.description}</td>
                <td className="px-6 py-4"> {study.content}</td>
                <td className="px-6 py-4"> {study.author}</td>
                <td className="px-6 py-4 flex justify-between">
                  <button
                    className="underline"
                    onClick={() => deleteCaseStudy(study.id)}
                  >{`DELETE`}</button>
                  <button
                    className="underline"
                    onClick={() => updateCaseStudy(study.id)}
                  >{`UPDATE`}</button>
                </td>
              </tr>
              {currentCaseStudy && currentCaseStudy.id === study.id && (
                <tr>
                  <td colSpan={6}>
                    <div className="p-4">
                      <h3 className="text-md font-semibold">Comments</h3>
                      <ul className="list-disc list-inside">
                        {comments.map((comment) => (
                          <li key={comment.id}>
                            {comment.content}
                            <button
                              className="ml-2 text-sm text-blue-500 hover:underline"
                              onClick={() =>
                                handleEditComment(comment.id, comment.content)
                              }
                            >
                              Edit
                            </button>
                            <button
                              className="ml-2 text-sm text-red-500 hover:underline"
                              onClick={() =>
                                handleDeleteComment(study.id, comment.id)
                              }
                            >
                              Delete
                            </button>
                            {editComment && currCommentId === comment.id && (
                              <button
                                className="ml-2 text-sm text-blue-500 hover:underline"
                                onClick={() =>
                                  submitUpdatedComment(study.id, comment.id)
                                }
                              >
                                Update Comment
                              </button>
                            )}
                          </li>
                        ))}
                      </ul>

                      <textarea
                        value={newComment}
                        onChange={handleNewCommentChange}
                        className="block w-full p-2 mt-2 text-gray-900 border border-gray-300 rounded-lg bg-gray-50 sm:text-xs focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                      />

                      {!editComment && (
                        <button
                          className="mt-2 bg-cyan-700 hover:bg-cyan-800 text-white font-bold py-2 px-4 rounded-full"
                          onClick={() => handleAddComment(study.id)}
                        >
                          {"Add Comment"}
                        </button>
                      )}
                    </div>
                  </td>
                </tr>
              )}
            </React.Fragment>
          ))}
        </tbody>
      </table>
    </div>
  );
}
