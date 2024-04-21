
import original from "file:///C:/Users/anand/OneDrive/Desktop/New%20folder/react/images/output/original.jpg"
import enhanced from "file:///C:/Users/anand/OneDrive/Desktop/New%20folder/react/images/output/enhanced.jpg"
import object from "file:///C:/Users/anand/OneDrive/Desktop/New%20folder/react/images/output/object.jpg"
export const Result=()=>{
    return (
        <>
        <div className="headerNew">
        </div>
        <div className="inner-header flex">
          
          <div className="containerWrapper">
            <h2 className="containerName"   > ORIGINAL</h2>
            <img src={original}></img>
          </div>
          <div className="containerWrapper">
            <h2 className="containerName" >ENHANCED</h2>
            <img src={enhanced}></img>
          </div>
          <div className="containerWrapper">
            <h2 className="containerName">DEBRIS DETECTED</h2>
            <img src={object}></img>
          </div>
         
          
        </div>
        </>

    );
}