import { Badge } from "@/components/ui/badge";

export function RecommendationBadge({ category }: { category: string }) {
  return <Badge>{category}</Badge>;
}
