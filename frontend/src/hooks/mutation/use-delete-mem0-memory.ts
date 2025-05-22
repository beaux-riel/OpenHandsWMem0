import { useMutation, useQueryClient } from "@tanstack/react-query";
import { apiClient } from "#/api/api-client";

export function useDeleteMem0Memory() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: async (memoryId: string) => {
      await apiClient.delete(`/api/mem0/memories/${memoryId}`);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["mem0", "memories"] });
    },
  });
}