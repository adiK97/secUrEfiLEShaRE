import React, { useEffect, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { downloadFile, getFileList, sendFile } from './Serverhandle/Apis'
export default function (props) {
    const location = useLocation()
    const [selectedFile, setSelectedFile] = useState();
    const [fileList, setFileList] = useState([]);
    const [isFilePicked, setIsFilePicked] = useState(false);
    const navigate = useNavigate()
    const changeHandler = (event) => {
        console.log('sdfasdf', event.target.files[0])
        setSelectedFile(event.target.files[0]);
        setIsFilePicked(true);
    };
    const [authUserList, setAuthUsers] = useState('')

    const handleSubmission = () => {
        var formdata = new FormData();
        formdata.append("file", selectedFile);
        formdata.append('users', authUserList)
        var requestOptions = {
            method: 'POST',
            body: formdata,
            redirect: 'follow'
        };

        fetch("http://192.168.1.149:4000/file", requestOptions)
            .then(response => response.text())
            .then(result => console.log(result))
            .catch(error => console.log('error', error));
    };

    useEffect(() => {
        getFileList().then((e) => {
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
                                <text>Authorized/Intended Users:
                                    <input
                                        type={'text'}
                                        value={authUserList}
                                        placeholder={'Comma seperated list of usernames...'}
                                        onChange={(e) => {
                                            setAuthUsers(e.target.value)
                                        }}
                                    />
                                </text>
                                <button onClick={handleSubmission}>Submit</button>
                            </div>
                        </div>
                    </form>
                    <button style={{ margin: 15 }} onClick={() => navigate('/')}>Logout, {location?.state?.username}</button>
                </div>
                <div style={{ display: 'flex', flex: 1, }}>
                    {/* <div className="Auth-form-container"> */}
                    <div className="Auth-form-content">
                        <h3 className="Auth-form-title">Uploaded File Directory</h3>
                        {fileList.map((filename) => {
                            return (
                                <div style={{ border: '1px solid grey' }}>
                                    <button onClick={() => { downloadFile(filename).then(alert('download started')) }}>{filename}</button>
                                </div>)
                        })}
                    </div>
                </div>
                {/* </div> */}
            </div>

        </>
    )
}