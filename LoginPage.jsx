import { useState } from "react";
import { useNavigate } from "react-router-dom";

import Button from "../../components/ui/Button.jsx";
import Card from "../../components/ui/Card.jsx";

import { login } from "./authApi";

import "../../components/forms/forms.css";

function LoginPage() {

    const navigate = useNavigate();

    const [username,setUsername] = useState("");
    const [password,setPassword] = useState("");

    const [error,setError] = useState("");

    async function handleLogin(e){

        e.preventDefault();

        try{

            const response = await login({
                username,
                password
            });

            localStorage.setItem(
                "access_token",
                response.data.access_token
            );

            navigate("/");

        }catch{

            setError("Usuario o contraseña incorrectos.");

        }

    }

    return(

        <div className="login-page">

            <Card title="Regulatory Platform">

                <form
                    className="simple-form"
                    onSubmit={handleLogin}
                >

                    <label>

                        Usuario

                        <input
                            value={username}
                            onChange={(e)=>setUsername(e.target.value)}
                        />

                    </label>

                    <label>

                        Contraseña

                        <input
                            type="password"
                            value={password}
                            onChange={(e)=>setPassword(e.target.value)}
                        />

                    </label>

                    {error && <p>{error}</p>}

                    <Button type="submit">

                        Iniciar sesión

                    </Button>

                </form>

            </Card>

        </div>

    );

}

export default LoginPage;
