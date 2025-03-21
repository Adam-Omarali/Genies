"use client";

import { useCart } from "@/context/CartContext";
import Image from "next/image";
import Link from "next/link";

export default function CartPage() {
  const { cartItems, removeFromCart, updateQuantity } = useCart();

  const subtotal = cartItems.reduce(
    (total, item) => total + item.price * item.quantity,
    0
  );

  if (cartItems.length === 0) {
    return (
      <div className="min-h-screen bg-gray-50 p-8">
        <div className="max-w-2xl mx-auto text-center">
          <h1 className="text-2xl font-bold text-gray-900 mb-4">Your Cart</h1>
          <p className="text-gray-600 mb-8">Your cart is empty</p>
          <Link
            href="/"
            className="inline-block bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition-colors"
          >
            Continue Shopping
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-2xl font-bold text-gray-900 mb-8">Your Cart</h1>

        <div className="bg-white rounded-lg shadow overflow-hidden mb-8">
          {cartItems.map((item) => (
            <div
              key={item.name}
              className="flex items-center gap-6 p-6 border-b border-gray-200 last:border-0"
            >
              {/* Book Image */}
              <div className="w-24 h-32 relative flex-shrink-0">
                <Image
                  src={`${process.env.NEXT_PUBLIC_BACKEND_URL}${item.img}`}
                  alt={item.name}
                  fill
                  className="object-cover rounded"
                />
              </div>

              {/* Book Details */}
              <div className="flex-grow">
                <h3 className="text-lg font-medium text-gray-900 mb-1">
                  {item.name}
                </h3>
                <p className="text-gray-600 mb-4">{item.author}</p>

                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-4">
                    {/* Quantity Controls */}
                    <div className="flex items-center gap-2">
                      <button
                        onClick={() =>
                          updateQuantity(item.name, item.quantity - 1)
                        }
                        className="w-8 h-8 rounded border border-gray-300 flex items-center justify-center hover:bg-gray-100 text-gray-700"
                      >
                        -
                      </button>
                      <span className="w-8 text-center">{item.quantity}</span>
                      <button
                        onClick={() =>
                          updateQuantity(item.name, item.quantity + 1)
                        }
                        className="w-8 h-8 rounded border border-gray-300 flex items-center justify-center hover:bg-gray-100 text-gray-700"
                      >
                        +
                      </button>
                    </div>

                    {/* Price */}
                    <div className="flex items-baseline gap-2">
                      <span className="text-lg font-medium text-gray-900">
                        ${(item.price * item.quantity).toFixed(2)}
                      </span>
                      {item.discount > 0 && (
                        <span className="text-sm text-red-600">
                          {(item.discount * 100).toFixed(2)}% off
                        </span>
                      )}
                    </div>
                  </div>

                  {/* Remove Button */}
                  <button
                    onClick={() => removeFromCart(item.name)}
                    className="text-gray-400 hover:text-red-600"
                  >
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      fill="none"
                      viewBox="0 0 24 24"
                      strokeWidth={1.5}
                      stroke="currentColor"
                      className="w-5 h-5"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        d="M14.74 9l-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 01-2.244 2.077H8.084a2.25 2.25 0 01-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 00-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 013.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 00-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 00-7.5 0"
                      />
                    </svg>
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Summary */}
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex justify-between items-center mb-6">
            <span className="text-lg font-medium text-gray-900">Subtotal</span>
            <span className="text-xl font-bold text-gray-900">
              ${subtotal.toFixed(2)}
            </span>
          </div>
          <button className="w-full bg-blue-600 text-white py-3 rounded-lg hover:bg-blue-700 transition-colors">
            Proceed to Checkout
          </button>
        </div>
      </div>
    </div>
  );
}
