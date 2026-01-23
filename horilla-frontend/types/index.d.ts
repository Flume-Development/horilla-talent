declare const process: {
  client: boolean
  server: boolean
  env: Record<string, string>
}

declare module 'js-cookie' {
  interface CookieAttributes {
    expires?: number | Date
    path?: string
    domain?: string
    secure?: boolean
    sameSite?: boolean | string
    [key: string]: any
  }

  const Cookies: {
    set(name: string, value: string, options?: CookieAttributes): string | undefined
    get(name: string): string | undefined
    remove(name: string, options?: CookieAttributes): void
    [key: string]: any
  }

  export default Cookies
}
