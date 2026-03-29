import React from 'react'

import { Main } from './../components/common/Main.jsx'
import { Container } from './../components/common/Container.jsx'

import './../styles/pages/Contact.css'

export const Contact = () => {
    return (   
        <Main className='contact'>
            <Container>
                <div className='contact__data'>
                    <h2>Contáctenos</h2>
                    <p><strong>Datos de contacto</strong></p>
                    <p><strong>Dirección postal:</strong>Calle 54 1168 Oficina 4 La Plata (B1704FFY), Buenos Aires, Argentina</p>
                    <p><strong>Teléfonos:</strong>(+54-221) 4123-8567/4123-8568</p>
                    <p><strong>WhatsApp:</strong>+54 9 221 8567-4123</p>
                    <p><strong>Sitio Web:</strong>www.funkoshop.com</p>
                    <p><strong>E-mail:</strong>comercial@funkoshop.com</p>
                    <p>
                        Formulario de Contacto
                        Por favor complete el formulario para dejar su consulta o comentario.
                    </p>
                </div>
            </Container>
        </Main>
    )
}