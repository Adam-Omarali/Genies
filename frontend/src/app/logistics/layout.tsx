import LogisticsNavbar from "@/components/LogisticsNavbar";

export default function LogisticsLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div>
      <LogisticsNavbar />
      {children}
    </div>
  );
}
