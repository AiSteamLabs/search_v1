import React, { FC } from "react";

export const Logo: FC = () => {
  return (
    <div className="flex gap-4 items-center justify-center cursor-default select-none relative">
      <div className="text-center font-medium text-2xl md:text-3xl text-zinc-950 relative text-nowrap">
        Crypto Search
      </div>
    </div>
  );
};
