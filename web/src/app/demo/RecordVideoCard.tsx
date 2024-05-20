import {
  CardTitle,
  CardDescription,
  CardHeader,
  CardContent,
  CardFooter,
  Card,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import Link from "next/link";
import { cn } from "@/lib/utils";

export default function RecordVideoCard({ className }: { className?: string }) {
  return (
    <Card className={cn("flex flex-col", className)}>
      <CardHeader>
        <CardTitle>Record Interview</CardTitle>
        <CardDescription>Start recording a new interview</CardDescription>
      </CardHeader>
      <CardContent className="flex flex-1"></CardContent>
      <CardFooter>
        <Button className="w-full" asChild>
          <Link href="/record">Record</Link>
        </Button>
      </CardFooter>
    </Card>
  );
}
