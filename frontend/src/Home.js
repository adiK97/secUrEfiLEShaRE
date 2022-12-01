import React, { useState } from 'react';

export default function () {
    const [selectedFile, setSelectedFile] = useState();
    const [isFilePicked, setIsFilePicked] = useState(false);

    const changeHandler = (event) => {
        setSelectedFile(event.target.files[0]);
        setIsFilePicked(true);
    };

    const handleSubmission = () => {
        const formData = new FormData();

        formData.append('File', selectedFile);

        fetch(
            'https://freeimage.host/api/1/upload?key=<YOUR_API_KEY>',
            {
                method: 'POST',
                body: formData,
            }
        )
            .then((response) => response.json())
            .then((result) => {
                console.log('Success:', result);
            })
            .catch((error) => {
                console.error('Error:', error);
            });
    };

    return (
        <>
            <div style={{ display: 'flex', flexDirection: 'row', width: '100%' }}>
                <div className="Auth-form-container" style={{ flex: 1 }}>
                    <form className="Auth-form">
                        <div className="Auth-form-content">
                            <h3 className="Auth-form-title">Upload a File</h3>
                            <input type="file" name="file" onChange={changeHandler} style={{ textAlign: 'center' }} />
                            {isFilePicked ? (
                                <div>
                                    <p>Filename: {selectedFile.name}</p>
                                    <p>Filetype: {selectedFile.type}</p>
                                    <p>Size in bytes: {selectedFile.size}</p>
                                    <p>
                                        lastModifiedDate:{' '}
                                        {selectedFile.lastModifiedDate.toLocaleDateString()}
                                    </p>
                                </div>
                            ) : (
                                <p style={{ display: 'flex', justifyContent: 'center', alignSelf: 'center' }}>Select a file to show details</p>
                            )}
                            <div style={{ textAlign: 'center' }}>
                                <button onClick={handleSubmission}>Submit</button>
                            </div>
                        </div>
                    </form>

                </div>
                <div style={{ display: 'flex', flex: 1,}}>
                    {/* <div className="Auth-form-container"> */}
                        <div className="Auth-form-content">
                            <h3 className="Auth-form-title">Upload File Directory</h3>
                            
                        </div>
                    </div>
                {/* </div> */}
            </div>

        </>
    )
}