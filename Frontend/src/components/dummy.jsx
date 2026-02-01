import axios from "axios";
import { useState, useEffect } from "react";

const Dummy = () => {

  const [name, setName] = useState("");
  const [content, setContent] = useState("");

  const getUser = async () => {
    try {
      const res = await axios.post("http://127.0.0.1:8000/ask", {
        message: "how is the weather in kandy"
      });

      console.log(res.data); // { name: "AI", content: "..." }

      setName(res.data.name);       // ✅ access object fields
      setContent(res.data.content); // ✅
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    getUser();
  }, []);

  return (
    <div>
      <h3>{name}</h3>
      <p>{content}</p>
    </div>
  );
};

export default Dummy;
