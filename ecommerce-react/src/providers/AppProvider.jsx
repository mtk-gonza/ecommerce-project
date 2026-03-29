import React from 'react'

import { CategoriesProvider } from './CategoriesProvider.jsx'
import { LicensesProvider } from './LicensesProvider.jsx'
import { RolesProvider } from './RolesProvider.jsx'
import { AuthProvider } from './AuthProvider.jsx'
import { CartProvider } from './CartProvider.jsx'
import { ProductsProvider } from './ProductsProvider.jsx'
import { UsersProvider } from './UsersProvider.jsx'
import { FavoritesProvider } from './FavoritesProvider.jsx'

export const AppProvider = ({ children }) => {
    return (
        <RolesProvider>
            <AuthProvider>
                <CartProvider>
                    <CategoriesProvider>
                        <LicensesProvider>
                            <ProductsProvider>
                                <UsersProvider>
                                    <FavoritesProvider>
                                        {children}
                                    </FavoritesProvider>
                                </UsersProvider>
                            </ProductsProvider>
                        </LicensesProvider>
                    </CategoriesProvider>
                </CartProvider>
            </AuthProvider>
        </RolesProvider>
    )
}