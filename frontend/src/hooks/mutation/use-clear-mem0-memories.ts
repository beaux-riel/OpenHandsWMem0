import { useMutation, useQueryClient } from "@tanstack/react-query";
import { apiClient } from "#/api/api-client";

export function useClearMem0Memories() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: async () => {
      await apiClient.delete("/api/mem0/memories");
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["mem0", "memories"] });
    },
  });
}