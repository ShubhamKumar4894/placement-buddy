import ProtectedRoute from "@/components/ProtectedRoute";
const ResumePage = () => {
  return (
    <ProtectedRoute>
      <div className="text-amber-950">Resume Page</div>
    </ProtectedRoute>
  );
};

export default ResumePage;
