import React from 'react'
import { Link } from 'react-router-dom'

import { Main } from './../components/common/Main.jsx'
import { Container } from '../components/common/Container.jsx'

import './../styles/pages/Terms.css'

export const Terms = () => {
    return (
        <Main className='terms'>
            <Container> 
                <div className='terms-content'>
                    <h1>Terminos y Condiciones</h1>
                    <p>
                        Bienvenido a Funkoshop. Al acceder y utilizar nuestro sitio web, aceptas cumplir con los siguientes términos y condiciones. Por favor, léelos atentamente antes de realizar cualquier compra o utilizar nuestros servicios.
                    </p>
                    <h3>2. Condiciones de Uso</h3>
                    <ul>
                        <li>El uso de este sitio está permitido solo para mayores de 18 años o menores con autorización de sus padres o tutores.</li>
                        <li>No está permitido utilizar el sitio para fines ilegales o no autorizados.</li>
                        <li>La información proporcionada debe ser verídica y actualizada.</li>
                    </ul>
                    <h3>3. Propiedad Intelectual</h3>
                    <ul>
                        <li>Todo el contenido de Funkoshop, incluyendo imágenes, textos, logos y diseños, es propiedad de Funkoshop o de sus licenciantes.</li>
                        <li>No está permitida la reproducción, distribución o uso del contenido sin autorización previa y por escrito.</li>
                    </ul>
                    <h3>4. Responsabilidad</h3>
                    <ul>
                        <li>Funkoshop no se responsabiliza por daños derivados del mal uso del sitio o de la información contenida en él.</li>
                        <li>Nos reservamos el derecho de modificar precios, productos y servicios sin previo aviso.</li>
                    </ul>
                    <h3>5. Modificaciones</h3>
                    <p>
                        Funkoshop puede modificar estos términos y condiciones en cualquier momento. Las modificaciones entrarán en vigor desde su publicación en el sitio.
                    </p>
                    <h3>6. Contacto</h3>
                    <p>
                        Si tienes dudas sobre estos términos y condiciones, puedes contactarnos a través de nuestro correo <a href="mailto:contacto@funkoshop.com">contacto@funkoshop.com</a> o por WhatsApp al +54 9 11 1234-5678.
                    </p>
                <Link className='link' to='/'>Volver</Link>               
                </div>
            </Container>
        </Main>
    )
}