"use client";
import { Dispatch, SetStateAction, useEffect, useState } from "react";
import { Dialog, DialogPanel, TextInput } from "@tremor/react";
import { RiCloseLine } from "@remixicon/react";

export default function ModalEnterMail({
  isOpen,
  setIsOpen,
  action,
}: {
  isOpen: boolean;
  setIsOpen: Dispatch<SetStateAction<boolean>>;
  action: (email: string) => Promise<void>;
}) {
  const [email, setEmail] = useState<string>("");

  return (
    <Dialog
      open={isOpen}
      onClose={() => setIsOpen(false)}
      static={true}
      className="z-[100]"
    >
      <DialogPanel className="sm:max-w-md">
        <div className="absolute right-0 top-0 pr-3 pt-3">
          <button
            type="button"
            className="rounded-tremor-small p-2 text-tremor-content-subtle hover:bg-tremor-background-subtle hover:text-tremor-content dark:text-dark-tremor-content-subtle hover:dark:bg-dark-tremor-background-subtle hover:dark:text-tremor-content"
            onClick={() => setIsOpen(false)}
            aria-label="Close"
          >
            <RiCloseLine className="h-5 w-5 shrink-0" aria-hidden={true} />
          </button>
        </div>

        <form action="#" method="POST">
          <h4 className="font-semibold text-tremor-content-strong dark:text-dark-tremor-content-strong">
            Your email
          </h4>
          <p className="mt-2 text-tremor-default leading-6 text-tremor-content dark:text-dark-tremor-content">
            We will send the results to your email
          </p>
          <TextInput
            name="user-email"
            type="email"
            className="mt-2"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
          <button
            type="submit"
            disabled={!email}
            className="mt-4 w-full whitespace-nowrap rounded-tremor-default bg-tremor-brand px-4 py-2 text-center text-tremor-default font-medium text-tremor-brand-inverted shadow-tremor-input hover:bg-tremor-brand-emphasis dark:bg-dark-tremor-brand dark:text-dark-tremor-brand-inverted dark:shadow-dark-tremor-input dark:hover:bg-dark-tremor-brand-emphasis"
            onClick={(e) => {
              e.preventDefault();
              action(email);
              setIsOpen(false);
            }}
          >
            Send Video
          </button>
        </form>
      </DialogPanel>
    </Dialog>
  );
}
