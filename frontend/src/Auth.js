import React, { useState } from "react"
import { createUserAPI, loginUserAPI } from "./Serverhandle/Apis"
import { ObjectsToArray } from "./utils"

export default function (props) {
  let [authMode, setAuthMode] = useState("signin")
  const [username, setUsername] = useState("")
  const [password, setPassword] = useState("")
  const changeAuthMode = () => {
    setAuthMode(authMode === "signin" ? "signup" : "signin")
  }

  const submit = () => {

    if (authMode == 'signin') loginUserAPI(username, password).then(e => console.log(e))
    else createUserAPI(username, password).then(e => console.log(e))
  }
  if (authMode === "signin") {
    return (
      <div className="Auth-form-container">
        <div className="Auth-form">
          <div className="Auth-form-content">
            <h3 className="Auth-form-title">Sign In</h3>
            <div className="text-center">
              Not registered yet?{" "}
              <span className="link-primary" onClick={changeAuthMode}>
                Sign Up
              </span>
            </div>
            <div className="form-group mt-3">
              <label>username</label>
              <input
                type="text"
                value={username}
                className="form-control mt-1"
                placeholder="username"
                onChange={(e) => setUsername(e.target.value)}
              />
            </div>
            <div className="form-group mt-3">
              <label>Password</label>
              <input
                type="password"
                value={password}
                className="form-control mt-1"
                placeholder="Enter password"
                onChange={(e) => setPassword(e.target.value)}
              />
            </div>
            <div className="d-grid gap-2 mt-3">
              <button type="submit" onClick={submit} className="btn btn-primary">
                Submit
              </button>
            </div>
            <p className="text-center mt-2">
            </p>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="Auth-form-container">
      <div className="Auth-form">
        <div className="Auth-form-content">
          <h3 className="Auth-form-title">Sign Up</h3>
          <div className="text-center">
            Already registered?{" "}
            <span className="link-primary" onClick={changeAuthMode}>
              Sign In
            </span>
          </div>
          <div className="form-group mt-3">
            <label>username</label>
            <input
              type="text"
              value={username}
              className="form-control mt-1"
              placeholder="Username"
              onChange={(e) => setUsername(e.target.value)}
            />
          </div>
          <div className="form-group mt-3">
            <label>Password</label>
            <input
              type="password"
              value={password}
              className="form-control mt-1"
              placeholder="Password"
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>
          <div className="d-grid gap-2 mt-3">
            <button onClick={submit} type="submit" className="btn btn-primary">
              Submit
            </button>
          </div>
          <p className="text-center mt-2">
          </p>
        </div>
      </div>
    </div>
  )
}