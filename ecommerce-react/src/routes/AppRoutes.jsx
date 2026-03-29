import React from 'react'
import { Routes, Route } from 'react-router-dom'

import { Home } from './../pages/Home.jsx'
import { Login } from './../pages/Login.jsx'
import { Register } from './../pages/Register.jsx'
import { Shop } from './../pages/Shop.jsx'
import { Detail } from './../pages/Detail.jsx'
import { Contact } from './../pages/Contact.jsx'
import { Favorites } from '../pages/Favorites.jsx'
import { Purchases } from './../pages/Purchases.jsx'
import { Dashboard } from './../pages/Dashboard.jsx'
import { Returns } from './../pages/Returns.jsx'
import { Terms } from './../pages/Terms.jsx'
import { Privacy } from './../pages/Privacy.jsx'
import { Unauthorized } from './../pages/Unauthorized.jsx'
import { NotFound } from './../pages/NotFound.jsx'

import { ProtectedRoute } from './ProtectedRoute.jsx'

export const AppRoutes = () => {
	return (
		<Routes>
			<Route path='/' element={<Home />} />
			<Route path='/login' element={<Login />} />
			<Route path='/register' element={<Register />} />
			<Route path='/shop' element={<Shop />} />
			<Route path='/shop/:category_name?/:license_id?' element={<Shop  />} />
			<Route path='/detail/:product_id?' element={<Detail/>} />
			<Route path='/contact' element={<Contact />} />
			<Route path='/favorites' element={<ProtectedRoute allowedRoles={['guest', 'admin']}> <Favorites/> </ProtectedRoute>} />
			<Route path='/purchases' element={<ProtectedRoute allowedRoles={['guest', 'admin']}> <Purchases/> </ProtectedRoute>} />
			<Route path='/dashboard' element={<ProtectedRoute allowedRoles={['admin']}> <Dashboard/> </ProtectedRoute>} />	
			<Route path='/returns' element={<ProtectedRoute allowedRoles={['guest', 'admin']}> <Returns/> </ProtectedRoute>} />		
			<Route path='/terms' element={<Terms/>} />		
			<Route path='/privacy' element={<Privacy/>} />		
			<Route path='/unauthorized'	element={<Unauthorized/>} />		
			<Route path='*' element={<NotFound />} />
		</Routes>
	)
}