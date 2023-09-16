import react ,{ useState } from 'react'

export default function TelaPrincipal()
{
    const [TextError , SetTextoError] = useState('');
    const [File      , SetFile      ] = useState();

    function PostImageTurmo( image ){
        alert('imagem em upload') 
        try{
            SetTextoError('');
            SetFile(
                URL.createObjectURL( 
                    image.target.files[0]
                    )

            );

        }catch(error){
            SetTextoError('Invalido tente novamente');
        }
    }
    return(
        <div>
            <h1>Projeto Breast Ultrasound</h1>

            <div>
                <p>{TextError}</p>
                <img  src={File}/>
            </div>
            <div>
                <input type="file" onChange={PostImageTurmo}></input>
            </div>
        

        </div>
    );
}