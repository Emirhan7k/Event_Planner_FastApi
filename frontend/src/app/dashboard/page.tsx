import { RecommendationFeed } from "@/components/ai/recommendation_feed";
import { DashboardLayout } from "@/components/layout/dashboard_layout";

export default function DashboardPage() {
  return (
    <DashboardLayout>
      <RecommendationFeed />
    </DashboardLayout>
  );
}
