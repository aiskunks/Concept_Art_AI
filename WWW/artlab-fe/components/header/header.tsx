import ThemeToggle from 'components/theme-toggle'
import Image from 'next/image'
import React from 'react'
import Logo from 'components/ui/Logo'

const Header = () => {
  return (
    <div className='fixed top-0 left-0 right-0 mx-auto max-w-6xl flex justify-between border-inherit rounded-lg px-4 py-2 items-center my-5 backdrop-blur-md bg-inherit bg-opacity-50 border border-zinc-200 shadow-sm dark:border-zinc-800'>
      <div className='flex items-center justify-center'>
        <Logo />
      </div>
      <div className='flex items-center justify-center space-x-4'>
       
        <ThemeToggle />
      </div>
    </div>
  )
}

export default Header