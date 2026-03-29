import React from 'react'
import { Link } from 'react-router-dom'

import { Main } from './../components/common/Main.jsx'
import { Container } from './../components/common/Container.jsx'

import './../styles/pages/Returns.css'

export const Returns = () => {
    return (
        <Main className='returns'>
            <Container>
                <div className='returns-content'>
                    <h1>Devoluciones</h1>
                    <h3>1. Introducción</h3>
                    <p>
                        En Funkoshop, queremos que estés satisfecho con tu compra. Si no estás conforme con algún producto, puedes solicitar una devolución siguiendo las condiciones y pasos que detallamos a continuación.
                    </p>
                    <h3>2. Condiciones para Devoluciones</h3>
                    <ul>
                        <li>El producto debe estar en su estado original, sin uso y con su empaque original.</li>
                        <li>Debes realizar la solicitud de devolución dentro de los 10 días hábiles posteriores a la recepción del pedido.</li>
                        <li>No se aceptan devoluciones de productos personalizados o en oferta, salvo que presenten fallas de fábrica.</li>
                    </ul>
                    <h3>3. Proceso de Devolución</h3>
                    <ol>
                        <li>Envía un correo a <a href="mailto:devoluciones@funkoshop.com">devoluciones@funkoshop.com</a> con tu número de pedido, motivo de la devolución y fotos del producto.</li>
                        <li>Nuestro equipo revisará tu solicitud y te responderá en un plazo de 48 horas hábiles.</li>
                        <li>Si la devolución es aprobada, te enviaremos las instrucciones para el envío del producto.</li>
                        <li>Una vez recibido y verificado el estado del producto, gestionaremos el reembolso o cambio según tu preferencia.</li>
                    </ol>
                    <h3>4. Costos de Envío</h3>
                    <ul>
                        <li>Si la devolución es por un error nuestro o defecto de fábrica, cubriremos los gastos de envío.</li>
                        <li>Si la devolución es por otro motivo, el costo de envío corre por cuenta del cliente.</li>
                    </ul>
                    <h3>5. Contacto</h3>
                    <p>
                        Si tienes dudas sobre el proceso, puedes contactarnos a través de nuestro correo <a href="mailto:devoluciones@funkoshop.com">devoluciones@funkoshop.com</a> o por WhatsApp al +54 9 11 1234-5678.
                    </p>
                    <Link className='link' to='/'>Volver</Link>     
                </div>
            </Container>
        </Main>
    )
}