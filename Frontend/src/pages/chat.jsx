import Msg from "../components/message";
//import socket from "../services/socket" 
import { useEffect,useState,useRef } from "react";
import axios from 'axios'
import api from "../Auth/axois";
import Navbar from "../components/Navbar";
import { useAuth } from "../Auth/AuthContext";


const Chat = () => {  
  

  //auth


  const [profile, setProfile] = useState(null);
  const { logout } = useAuth();
  


  useEffect(() => {
    /*
    Axios automatically sends JWT
    */
    api.get("/profile")
      .then(res => setProfile(res.data))
      .catch(() => {
        // token invalid or expired
        logout();
      });
  }, []);

  //end auth


  const data = { "user": "Himasha", "content": "hello" }
  
 

  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  

    useEffect(()=>{
      const get_messages = async() =>{
        try {
        const res = await api.get("/all_messages");
        console.log(res.data)
        setMessages(res.data); 
      } catch (err) {
        console.error("fetch messages failed:", err);
      }
      }

      get_messages()
  },[]);
  
  
    const sendMessage = async () => {
      if (!input.trim()) return;
      console.log("ran")
      try {
        const res = await api.post("/ask", {
          message: input
        });
        console.log("from chatr", res.data)
        setMessages((prev) => [...prev, ...res.data]);
        setInput("");
      } catch (err) {
        console.error("Send message failed:", err);
      }
    };
// image upload

  const [pendingFile, setPendingFile] = useState(null);
  const fileInputRef = useRef(null);


    const handleUpload = () =>{
      fileInputRef.current.click();
    }

    const handleChange = async(e) =>{
      const file = e.target.files[0];

      if (!file) return;

      window.alert("file uploaded")
      setPendingFile(file);
    }

    const sendImage = async() =>{

      if(!pendingFile) return;

      

      const formdata = new FormData()
      formdata.append("image",pendingFile)

      try{
        const res = await api.post("/upload-image", formdata,{
            headers: {
          "Content-Type": "multipart/form-data",
          },
        })

      window.alert("file uploaded")

      }catch(err){
        console.error("Image upload failed:", err);
      }
    }

   
     /*

    socket.on("reply", handleReply);

    // emit only when connected
    const onConnect = () => {
      console.log("Socket connected:", socket.id);
      socket.emit("Ask", { user: "Himasha", content: "hello" });
    };

    if (!socket.connected) {
      socket.connect();       // start connection
      socket.on("connect", onConnect);
    } else {
      socket.emit("Ask", { user: "Himasha", content: "hello" });
    }

    return () => {
      socket.off("reply", handleReply);
      socket.off("connect", onConnect);
    };
  }, []);

  useEffect(()=>{

    socket.on('connect',()=>{
      setIsConnected(socket.connected)
    })

      socket.on('disconnect',()=>{
      setIsConnected(socket.connected)
    })


  }
  )*/
   


  



    return ( 

 <div className="h-screen flex flex-col overflow-hidden">

    {/* Navbar */}
    <Navbar />
      
        <div className="flex h-screen antialiased text-gray-800  p-0">

        
        <div className="flex flex-row h-full w-full overflow-x-hidden">
          
          <div className="flex flex-col py-8 pl-6 pr-2 w-64 bg-white flex-shrink-0">
            
         <div className="flex flex-row items-center justify-center h-12 w-full">
  <div className="flex items-center justify-center rounded-2xl text-emerald-600 bg-emerald-50 h-10 w-10">
    <svg
      className="w-6 h-6"
      fill="none"
      stroke="currentColor"
      viewBox="0 0 24 24"
      xmlns="http://www.w3.org/2000/svg"
    >
      <path
        strokeLinecap="round"
        strokeLinejoin="round"
        strokeWidth="2"
        d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"
      ></path>
    </svg>
  </div>
  <div className="ml-2 font-bold text-2xl text-gray-800">QuickChat</div>
</div>

<div className="flex flex-col mt-8">
  <button className="flex flex-row items-center hover:bg-emerald-50 rounded-xl p-2 transition-colors duration-200">
    <div className="ml-2 text-sm font-semibold text-emerald-700">New Chat</div>
  </button>

  <div className="flex flex-col space-y-1 mt-4 -mx-2 h-140 overflow-y-auto">
    <button className="flex flex-row items-center hover:bg-gray-50 rounded-xl p-2 transition-colors duration-200">
      <div className="ml-2 text-sm font-semibold text-gray-700">Henry Boyd</div>
    </button>
    <button className="flex flex-row items-center hover:bg-gray-50 rounded-xl p-2 transition-colors duration-200">
      <div className="ml-2 text-sm font-semibold text-gray-700">Marta Curtis</div>
    </button>
    <button className="flex flex-row items-center hover:bg-gray-50 rounded-xl p-2 transition-colors duration-200">
      <div className="ml-2 text-sm font-semibold text-gray-700">Philip Tucker</div>
    </button>
    <button className="flex flex-row items-center hover:bg-gray-50 rounded-xl p-2 transition-colors duration-200">
      <div className="ml-2 text-sm font-semibold text-gray-700">Christine Reid</div>
    </button>
    <button className="flex flex-row items-center hover:bg-gray-50 rounded-xl p-2 transition-colors duration-200">
      <div className="ml-2 text-sm font-semibold text-gray-700">Jerry Guzman</div>
    </button>
    <button className="flex flex-row items-center hover:bg-gray-50 rounded-xl p-2 transition-colors duration-200">
      <div className="ml-2 text-sm font-semibold text-gray-700">Russell Williams</div>
    </button>
    <button className="flex flex-row items-center hover:bg-gray-50 rounded-xl p-2 transition-colors duration-200">
      <div className="ml-2 text-sm font-semibold text-gray-700">Elizabeth Garcia</div>
    </button>
    <button className="flex flex-row items-center hover:bg-gray-50 rounded-xl p-2 transition-colors duration-200">
      <div className="ml-2 text-sm font-semibold text-gray-700">Bruce Reid</div>
    </button>
    <button className="flex flex-row items-center hover:bg-gray-50 rounded-xl p-2 transition-colors duration-200">
      <div className="ml-2 text-sm font-semibold text-gray-700">Louis Crawford</div>
    </button>
    <button className="flex flex-row items-center hover:bg-gray-50 rounded-xl p-2 transition-colors duration-200">
      <div className="ml-2 text-sm font-semibold text-gray-700">{
        pendingFile?
        <div>yes</div>:<div>no</div>
        
        }</div>
    </button>
  </div>
</div>
          </div>

          <div className="flex flex-col flex-auto h-full p-6">
            
            <div className="flex flex-col flex-auto flex-shrink-0 rounded-2xl bg-gray-100 h-full p-4">
              
              <div className="w-full p-4 mb-2 bg-emerald-100 text-emerald-800 rounded-xl text-center font-semibold shadow-sm">
                Welcome, {profile?.name || "User"}! How can I help you today?
              </div>



              <div className="flex flex-col h-full overflow-x-auto mb-4">
                <div className="flex flex-col h-full">

                  <div className="grid grid-cols-12 gap-y-2">

                
                    
                    
                    
                    {messages.map((msg, index) => (
                      <Msg key={msg._id} content={msg} />
                    ))}


                  
                   

                   
                    
                    

                   


                  </div>



                  {pendingFile && (
                    <div className="flex items-center justify-between bg-white px-4 py-2 rounded-lg mb-2 shadow-sm">
                      <span className="text-sm truncate">
                        📎 {pendingFile.name}
                      </span>
                      <button
                        onClick={() => {
                          setPendingFile(null);
                          fileInputRef.current.value = "";
                        }}
                        className="text-red-500"
                      >
                        ✕
                      </button>
                    </div>
                  )}




                </div>
              </div>

              <div className="flex flex-row items-center h-16 rounded-xl bg-white w-full px-4 mb-4">
                <div>

                  
                  <div>
                    {/* Hidden file input */}
                    <input
                      type="file"
                      accept="image/*"
                      ref={fileInputRef}
                      onChange={handleChange}
                      className="hidden"
                    />

                    {/* Upload icon */}
                    <button
                      type="button"
                      onClick={handleUpload}
                      className="flex items-center justify-center text-gray-400 hover:text-emerald-600 transition"
                    >
                      <svg
                        className="w-5 h-5"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                      >
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          strokeWidth="2"
                          d="M15.172 7l-6.586 6.586a2 2 0 102.828 2.828l6.414-6.586a4 4 0 00-5.656-5.656l-6.415 6.585a6 6 0 108.486 8.486L20.5 13"
                        />
                      </svg>
                    </button>
                  </div>

                </div>

                <div className="flex-grow ml-4">
                  <div className="relative w-full">
                    <input
                      type="text"
                      value={input}
                      onChange={(e) => setInput(e.target.value)}
                      className="flex w-full border rounded-xl focus:outline-none focus:border-green-300 pl-4 h-10"
                    />
                    <button className="absolute flex items-center justify-center h-full w-12 right-0 top-0 text-gray-400 hover:text-gray-600">
                      <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          strokeWidth="2"
                          d="M14.828 14.828a4 4 0 01-5.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                        ></path>
                      </svg>
                    </button>
                  </div>
                </div>

                <div className="ml-4 ">
                  <button className="flex items-center justify-center bg-emerald-600 hover:bg-green-700 rounded-xl text-white px-4 py-1 flex-shrink-0"  onClick={sendMessage}>
                    <span>Send</span>
                    <span className="ml-2">
                      <svg
                        className="w-4 h-4 transform rotate-45 -mt-px"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                        xmlns="http://www.w3.org/2000/svg"
                      >
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          strokeWidth="2"
                          d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"
                        ></path>
                      </svg>
                    </span>
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
</div>

     );
}
 
export default Chat;