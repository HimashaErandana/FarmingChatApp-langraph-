const Msg = ({content}) => {
    
    console.log("from smg",content)
    const name = content["user"]
    const con = content["content"]
    const n = name.charAt(0)
    var a = true;
    if(name == 'AI'){
        a = true
    }else{
        a = false
    }
    
    return ( 

         <>
         {a?
          <div className="col-start-1 col-end-8 p-3 rounded-lg">
                      <div className="flex flex-row items-center">
                        <div className="flex items-center justify-center h-10 w-10 rounded-full bg-green-500 flex-shrink-0">AI</div>
                        <div className="relative ml-3 text-sm bg-white py-2 px-4 shadow rounded-xl">
                          <div>{con}</div>
                        </div>
                      </div>
            </div>
         :


         <div className="col-start-6 col-end-13 p-3 rounded-lg">
                    <div className="flex items-center justify-start flex-row-reverse">
                      <div className="flex items-center justify-center h-10 w-10 rounded-full bg-green-500 flex-shrink-0">{n}</div>
                      <div className="relative mr-3 text-sm bg-green-100 py-2 px-4 shadow rounded-xl">
                        <div>{con}</div>
                      </div>
                    </div>
                  </div>

        }
         </>

     );
}
 
export default Msg;



                  