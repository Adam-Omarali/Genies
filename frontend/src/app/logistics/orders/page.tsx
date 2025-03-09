"use client";

import { useState } from "react";

function Spinner() {
  return (
    <div className="flex justify-center items-center h-[500px] bg-white rounded-lg shadow">
      <div className="animate-spin rounded-full h-16 w-16 border-t-2 border-b-2 border-blue-600"></div>
    </div>
  );
}

export default function OrdersPage() {
  const [mode, setMode] = useState<"known" | "unknown">("unknown");
  const [numTrucks, setNumTrucks] = useState("3");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [routesImage, setRoutesImage] = useState<string | null>(null);
  const minTrucks = 1;
  const maxTrucks = 6;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    try {
      setIsLoading(true);
      setError(null);
      setRoutesImage(null);

      const formData = new FormData();
      formData.append("mode", mode === "known" ? "supervised" : "unsupervised");
      formData.append("num_trucks", mode === "known" ? numTrucks : "0");

      const response = await fetch(
        `${process.env.NEXT_PUBLIC_BACKEND_URL}/routes`,
        {
          method: "POST",
          body: formData,
        }
      );

      if (!response.ok) {
        throw new Error("Failed to generate routes");
      }

      const blob = await response.blob();
      const reader = new FileReader();
      reader.onloadend = () => {
        setRoutesImage(reader.result as string);
      };
      reader.readAsDataURL(blob);
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Failed to generate routes"
      );
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-2xl mx-auto">
        <h1 className="text-2xl font-bold text-gray-900 mb-8">Orders</h1>

        {error && (
          <div className="mb-4 p-4 text-red-700 bg-red-100 rounded-lg">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-4">
              Number of Trucks
            </label>
            <div className="flex gap-4">
              <button
                type="button"
                onClick={() => setMode("known")}
                className={`px-4 py-2 rounded-lg ${
                  mode === "known"
                    ? "bg-blue-600 text-white"
                    : "bg-white text-gray-700 border border-gray-300"
                }`}
              >
                Known
              </button>
              <button
                type="button"
                onClick={() => setMode("unknown")}
                className={`px-4 py-2 rounded-lg ${
                  mode === "unknown"
                    ? "bg-blue-600 text-white"
                    : "bg-white text-gray-700 border border-gray-300"
                }`}
              >
                Unknown
              </button>
            </div>
          </div>

          {mode === "known" && (
            <div className="space-y-4">
              <div className="flex justify-between items-center">
                <label
                  htmlFor="numTrucks"
                  className="block text-sm font-medium text-gray-700"
                >
                  Enter Number of Trucks
                </label>
                <span className="text-sm text-gray-500">{numTrucks}</span>
              </div>
              <div className="relative">
                <input
                  type="range"
                  id="numTrucks"
                  min={minTrucks}
                  max={maxTrucks}
                  value={numTrucks}
                  onChange={(e) => setNumTrucks(e.target.value)}
                  className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-blue-600"
                />
                <div className="flex justify-between text-xs text-gray-500 mt-2">
                  <span>{minTrucks}</span>
                  <span>{maxTrucks}</span>
                </div>
              </div>
            </div>
          )}

          <button
            type="submit"
            disabled={isLoading}
            className={`w-full py-2 px-4 rounded-lg text-white transition-colors ${
              isLoading
                ? "bg-blue-400 cursor-not-allowed"
                : "bg-blue-600 hover:bg-blue-700"
            }`}
          >
            {isLoading ? "Generating..." : "Generate Routes"}
          </button>
        </form>

        {(isLoading || routesImage) && (
          <div className="mt-8">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">
              Generated Routes
            </h2>
            {isLoading ? (
              <Spinner />
            ) : (
              <div className="relative w-full h-[500px] bg-white rounded-lg shadow overflow-hidden">
                <img
                  src={routesImage || ""}
                  alt="Generated Routes"
                  className="object-contain w-full h-full"
                />
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
