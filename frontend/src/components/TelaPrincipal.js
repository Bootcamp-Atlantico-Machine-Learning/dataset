import { useState } from 'react';
import DataBase from './firebase/firebase-config';
import {  ref ,uploadBytes } from 'firebase/storage';



export default function TelaPrincipal()
{
    const [File      , SetFile         ] = useState(null);
    const [FileFirebase,setFileFirebase] = useState(null);

    function PostImageTurmo(){
        if (File != null){   
            const image = ref(DataBase,'files.png');
            uploadBytes(image,FileFirebase);
        }
        
    }
    const loadImage = (image) =>{
        SetFile(URL.createObjectURL(image.target.files[0]));
        setFileFirebase(image.target.files[0]);
    }
    

    return(
        <div>
            <h1> hello world</h1>
            <h1>Projeto Breast Ultrasound</h1>

            <div>
                <img  src={File}/>
            </div>
            <div>
                <input type="file" onChange={(image)=>loadImage(image)}></input>
            </div>
            <div>
                <button onClick={PostImageTurmo} title='Continuar'>

                    Continuar
                </button>
            </div>


        </div>
    );
}