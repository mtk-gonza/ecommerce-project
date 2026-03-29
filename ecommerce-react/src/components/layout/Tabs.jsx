import React, { useState } from 'react'

import { Container } from './../common/Container.jsx'
import { Button } from './../common/Button.jsx'
import { Modal } from './../common/Modal.jsx'
import { ProductForm } from './../forms/ProductForm.jsx'
import { LicenseForm } from './../forms/LicenseForm.jsx'
import { CategoryForm } from './../forms/CategoryForm.jsx'
import { RoleForm } from './../forms/RoleForm.jsx'
import { UserForm } from './../forms/UserForm.jsx'
import { Products } from './Products.jsx'
import { Licenses } from './Licenses.jsx'
import { Categories } from './Categories.jsx'
import { Roles } from './Roles.jsx'
import { Users } from './Users.jsx'

import './../../styles/components/layouts/Tabs.css'

export const Tabs = () => {
    const [activeTab, setActiveTab] = useState(0)
    const [isOpen, setIsOpen] = useState(false)
    const [modalToShow, setModalToShow] = useState(null)

    const tabs = [
        { label: 'Productos', content: <Products /> },
        { label: 'Licencias', content: <Licenses /> },
        { label: 'Categorias', content: <Categories /> },
        { label: 'Roles', content: <Roles /> },
        { label: 'Usuarios', content: <Users /> }
    ]

    const handlerAdd = () => {
        setIsOpen(true)
        switch (tabs[activeTab].label) {
            case 'Productos':
                setModalToShow('product')
                break
            case 'Licencias':
                setModalToShow('license')
                break
            case 'Categorias':
                setModalToShow('category')
                break
            case 'Roles':
                setModalToShow('role')
                break
            case 'Usuarios':
                setModalToShow('user')
                break
            default:
                console.log('error')
                break
        }
    }

    const handleClosed = () => {
        setIsOpen(false)
    }

    return (
        <div className='tabs'>
            <Container>
                <div className='tabs__content'>
                    <div className='tabs__header'>
                        {tabs.map((tab, index) => (
                            <button
                                key={index}
                                onClick={() => setActiveTab(index)}
                                className={activeTab === index ? 'tab tab__active' : 'tab'}
                            >
                                {tab.label}
                            </button>
                        ))}
                        <div className='tab__add'>
                            <Button className='btn btn-add' onClick={handlerAdd}>
                                Agregar
                            </Button>
                        </div>
                    </div>
                    <div className='tab-content'>
                        {tabs[activeTab].content}
                    </div>
                </div>
            </Container>
            {isOpen &&
                <Modal isOpen={isOpen} onClosed={handleClosed}>
                    {modalToShow === 'product' && <ProductForm onClosed={handleClosed}/>}
                    {modalToShow === 'license' && <LicenseForm onClosed={handleClosed}/>}
                    {modalToShow === 'category' && <CategoryForm onClosed={handleClosed}/>}
                    {modalToShow === 'role' && <RoleForm onClosed={handleClosed}/>}
                    {modalToShow === 'user' && <UserForm onClosed={handleClosed}/>}
                </Modal>
            }
        </div>
    )
}