const Msg = ({content,img}) => {
    
    console.log("from smg",content.msgType)

   
    const name = content["msgType"]
    const text = content["message"]
    //const n = name.charAt(0)
   const isAI = content.msgType === "AI";
   const imgUrl = img //&& img.trim() !== "" ? img : null;




    return ( 

         <>
         {isAI?
          
          
          <div className="col-start-1 col-end-8 p-3 rounded-lg">

                      <div className="flex flex-row items-center">
                        <div className="flex items-center justify-center h-10 w-10 rounded-full bg-gradient-to-r from-green-500 to-emerald-600 flex-shrink-0 text-white font-bold shadow-md transform hover:scale-105 transition-transform duration-200">
                          AI
                        </div>


                        <div className="relative ml-3 text-sm bg-gray-200 py-2 px-4 shadow rounded-xl font-medium text-gray-900 leading-relaxed">
                          <div>{text}</div>
                        </div>
                      </div>
            </div>

           

         :


        




                   <div className="col-start-6 col-end-13 p-3 rounded-lg">
          <div className="flex items-center justify-start flex-row-reverse">
            <div className="flex items-center justify-center h-10 w-10 rounded-full bg-gradient-to-r from-green-500 to-emerald-600 flex-shrink-0 text-white font-bold shadow-md transform hover:scale-105 transition-transform duration-200">
                          U
                        </div>



            <div className="relative mr-3 text-sm bg-gradient-to-r from-green-100 to-emerald-50 border border-green-200 py-2 px-4 shadow rounded-xl max-w-md">
              
              {/* text */}
              {text && <div className="mb-2 font-semibold text-gray-800 mb-2 leading-relaxed">{text}</div>}

              {/* image (only if exists) */}
              {imgUrl && (
                <img
                  src={imgUrl}
                  alt="uploaded"
                  className="rounded-lg max-w-[220px] cursor-pointer"
                  onClick={() =>
                    window.open(imgUrl, "_blank")
                  }
                />
              )}
            </div>
          </div>
        </div>
        }
         </>

     );
}
 
export default Msg;



                  