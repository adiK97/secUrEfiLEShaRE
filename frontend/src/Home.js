import React, { useEffect, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { getFileList, sendFile } from './Serverhandle/Apis'
export default function (props) {
    const location = useLocation()
    const [selectedFile, setSelectedFile] = useState();
    const [fileList, setFileList] = useState([]);
    const [isFilePicked, setIsFilePicked] = useState(false);
    const navigate = useNavigate()
    const changeHandler = (event) => {
        setSelectedFile(event.target.files[0]);
        setIsFilePicked(true);
    };

    const handleSubmission = () => {
        const formData = new FormData();
        formData.append('file', selectedFile);
        sendFile(formData).catch(alert)
    };

    useEffect(() => {
        getFileList().then((e)=>{
            setFileList(e)
            console.log(e)
        })
    }, [])
    return (
        <>
            <div style={{ display: 'flex', flexDirection: 'row', width: '100%' }}>
                <div className="Auth-form-container" style={{ flex: 1, flexDirection: 'column' }}>
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
                    <button style={{ margin: 15 }} onClick={() => navigate('/')}>Logout, {location?.state?.username}</button>
                </div>
                <div style={{ display: 'flex', flex: 1, }}>
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