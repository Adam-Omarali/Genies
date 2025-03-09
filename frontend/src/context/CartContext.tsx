"use client";

import { createContext, useContext, useState, ReactNode } from "react";

interface CartItem {
  name: string;
  author: string;
  price: number;
  discount: number;
  img: string;
  quantity: number;
}

interface CartContextType {
  cartItems: CartItem[];
  cartItemsCount: number;
  addToCart: (book: Omit<CartItem, "quantity">) => void;
  removeFromCart: (bookName: string) => void;
  updateQuantity: (bookName: string, quantity: number) => void;
}

const CartContext = createContext<CartContextType | undefined>(undefined);

export function CartProvider({ children }: { children: ReactNode }) {
  const [cartItems, setCartItems] = useState<CartItem[]>([]);

  const cartItemsCount = cartItems.reduce(
    (total, item) => total + item.quantity,
    0
  );

  const addToCart = (book: Omit<CartItem, "quantity">) => {
    setCartItems((prevItems) => {
      const existingItem = prevItems.find((item) => item.name === book.name);
      if (existingItem) {
        return prevItems.map((item) =>
          item.name === book.name
            ? { ...item, quantity: item.quantity + 1 }
            : item
        );
      }
      return [...prevItems, { ...book, quantity: 1 }];
    });
  };

  const removeFromCart = (bookName: string) => {
    setCartItems((prevItems) =>
      prevItems.filter((item) => item.name !== bookName)
    );
  };

  const updateQuantity = (bookName: string, quantity: number) => {
    if (quantity < 1) {
      removeFromCart(bookName);
      return;
    }
    setCartItems((prevItems) =>
      prevItems.map((item) =>
        item.name === bookName ? { ...item, quantity } : item
      )
    );
  };

  return (
    <CartContext.Provider
      value={{
        cartItems,
        cartItemsCount,
        addToCart,
        removeFromCart,
        updateQuantity,
      }}
    >
      {children}
    </CartContext.Provider>
  );
}

export function useCart() {
  const context = useContext(CartContext);
  if (context === undefined) {
    throw new Error("useCart must be used within a CartProvider");
  }
  return context;
}
