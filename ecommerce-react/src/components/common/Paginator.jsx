import React from 'react'
import { Link } from 'react-router-dom'
import { faChevronLeft, faChevronRight } from '@fortawesome/free-solid-svg-icons'

import { Icon } from './Icon'

import './../../styles/components/common/Paginator.css'

export const Paginator = ({ currentPage, totalPages, onPageChange }) => {
    if (totalPages <= 1) return null

    const handlePageDecrease = (e) => {
        e.preventDefault()
        onPageChange(currentPage > 1 ? currentPage - 1 : 1)
    }

    const handlePageNumber = (e, pageNumber) => {
        e.preventDefault()
        onPageChange(pageNumber)   
    }

    const handlePageIncrease = (e) => {
        e.preventDefault()
        onPageChange(currentPage < totalPages ? currentPage + 1 : totalPages)
    }

    return (
        <div className='paginator'>
            <Link
                to={`#${currentPage > 1 ? currentPage - 1 : 1}`}
                className={`paginator__link ${currentPage === 1 ? 'disabled' : ''}`}
                onClick={handlePageDecrease}
                aria-disabled={currentPage === 1}
                tabIndex={currentPage === 1 ? -1 : 0}
            >
                <Icon css='icon' icon={faChevronLeft} />
            </Link>
            {[...Array(totalPages)].map((_, i) => {
                const pageNumber = i + 1
                return (
                    <Link
                        key={pageNumber}
                        to={`#${pageNumber}`}
                        className={`paginator__link ${currentPage === pageNumber ? 'paginator__link--selected' : ''}`}
                        onClick={(e) => handlePageNumber(e, pageNumber)}
                    >
                        {pageNumber}
                    </Link>
                )
            })}
            <Link
                to={`#${currentPage < totalPages ? currentPage + 1 : totalPages}`}
                className={`paginator__link ${currentPage === totalPages ? 'disabled' : ''}`}
                onClick={handlePageIncrease}
                aria-disabled={currentPage === totalPages}
                tabIndex={currentPage === totalPages ? -1 : 0}
            >
                <Icon css='icon' icon={faChevronRight} />
            </Link>
        </div>
    )
}