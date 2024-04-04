import { SVGProps } from "react";
import Link from "next/link";

function Component() {
  return (
    <div className="flex min-h-[100dvh] flex-col">
      <header className="border-b px-4 lg:px-6 flex h-16 items-center">
        <div className="mx-auto flex max-w-6xl items-center justify-between w-full">
          <div className="flex items-center space-x-2">
            <ScanFaceIcon className="h-6 w-6" />
            <h1 className="text-2xl font-bold">Face Emotion Recognition</h1>
          </div>
        </div>
      </header>
      <main className="flex-1">
        <section className="w-full py-12 md:py-24 lg:py-32">
          <div className="container px-4 md:px-6">
            <div className="mx-auto max-w-6xl space-y-12">
              <div className="grid items-center gap-6 lg:grid-cols-2 lg:gap-12">
                <img
                  alt="Face Emotion Recognition"
                  className="mx-auto aspect-video overflow-hidden rounded-xl object-cover object-center sm:w-full"
                  height="400"
                  src="/fer.png"
                  width="650"
                />
                <div className="space-y-4">
                  <h2 className="text-3xl font-bold tracking-tighter sm:text-5xl">
                    Enhance Your Hiring Process
                  </h2>
                  <p className="text-gray-500 md:text-xl/relaxed lg:text-base/relaxed xl:text-xl/relaxed dark:text-gray-400">
                    Our face emotion recognition technology provides deep
                    insights into candidate emotions and behaviors during job
                    interviews, helping you make more informed and unbiased
                    hiring decisions.
                  </p>
                  <ul className="grid gap-2 text-gray-500 dark:text-gray-400">
                    <li>
                      <CheckIcon className="mr-2 inline-block h-4 w-4" />
                      Accurately assess candidate engagement and enthusiasm
                    </li>
                    <li>
                      <CheckIcon className="mr-2 inline-block h-4 w-4" />
                      Identify potential biases and make fairer evaluations
                    </li>
                    <li>
                      <CheckIcon className="mr-2 inline-block h-4 w-4" />
                      Gain deeper insights into candidate traits and abilities
                    </li>
                  </ul>
                </div>
              </div>
              <div className="mx-auto max-w-6xl space-y-12">
                <div className="grid items-center gap-6 lg:grid-cols-2 lg:gap-12">
                  <div className="space-y-4">
                    <h2 className="text-3xl font-bold tracking-tighter sm:text-5xl">
                      How It Works
                    </h2>
                    <p className="text-gray-500 md:text-xl/relaxed lg:text-base/relaxed xl:text-xl/relaxed dark:text-gray-400">
                      Our face emotion recognition technology is seamlessly
                      integrated into the interview process, providing real-time
                      insights to help you make more informed hiring decisions.
                    </p>
                    <ol className="grid gap-4 text-gray-500 dark:text-gray-400">
                      <li>
                        <div className="flex items-start gap-2">
                          <div className="mt-1 rounded-full bg-gray-900 px-2 py-1 text-xs font-medium text-gray-50 dark:bg-gray-50 dark:text-gray-900">
                            1
                          </div>
                          <div>
                            <h3 className="text-lg font-semibold">
                              Candidate Consent
                            </h3>
                            <p>
                              Candidates are informed and must consent to the
                              use of face emotion recognition technology during
                              the interview.
                            </p>
                          </div>
                        </div>
                      </li>
                      <li>
                        <div className="flex items-start gap-2">
                          <div className="mt-1 rounded-full bg-gray-900 px-2 py-1 text-xs font-medium text-gray-50 dark:bg-gray-50 dark:text-gray-900">
                            2
                          </div>
                          <div>
                            <h3 className="text-lg font-semibold">
                              Real-time Monitoring
                            </h3>
                            <p>
                              Our AI-powered face emotion recognition system
                              monitors the candidate's facial expressions and
                              body language throughout the interview.
                            </p>
                          </div>
                        </div>
                      </li>
                      <li>
                        <div className="flex items-start gap-2">
                          <div className="mt-1 rounded-full bg-gray-900 px-2 py-1 text-xs font-medium text-gray-50 dark:bg-gray-50 dark:text-gray-900">
                            3
                          </div>
                          <div>
                            <h3 className="text-lg font-semibold">
                              Insightful Reports
                            </h3>
                            <p>
                              Receive comprehensive reports with detailed
                              insights into the candidate's emotional state,
                              engagement levels, and potential biases.
                            </p>
                          </div>
                        </div>
                      </li>
                    </ol>
                  </div>
                  <img
                    alt="How It Works"
                    className="mx-auto aspect-video overflow-hidden rounded-xl object-cover object-center sm:w-full"
                    height="400"
                    src="/fer2.jpg"
                    width="650"
                  />
                </div>
              </div>
              <div className="mx-auto max-w-6xl space-y-4 text-center">
                <h2 className="text-3xl font-bold tracking-tighter sm:text-5xl">
                  Get Started Today
                </h2>
                <p className="text-gray-500 md:text-xl/relaxed lg:text-base/relaxed xl:text-xl/relaxed dark:text-gray-400">
                  Experience the power of face emotion recognition in your
                  hiring process. Schedule a demo or contact our sales team to
                  learn more.
                </p>
                <div className="flex justify-center gap-2">
                  <Link
                    className="inline-flex h-10 items-center justify-center rounded-md bg-gray-900 px-8 text-sm font-medium text-gray-50 shadow transition-colors hover:bg-gray-900/90 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-gray-950 disabled:pointer-events-none disabled:opacity-50 dark:bg-gray-50 dark:text-gray-900 dark:hover:bg-gray-50/90 dark:focus-visible:ring-gray-300"
                    href="#"
                  >
                    Schedule a Demo
                  </Link>
                  <Link
                    className="inline-flex h-10 items-center justify-center rounded-md border border-gray-200 border-gray-200 bg-white px-8 text-sm font-medium shadow-sm transition-colors hover:bg-gray-100 hover:text-gray-900 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-gray-950 disabled:pointer-events-none disabled:opacity-50 dark:border-gray-800 dark:border-gray-800 dark:bg-gray-950 dark:hover:bg-gray-800 dark:hover:text-gray-50 dark:focus-visible:ring-gray-300"
                    href="#"
                  >
                    Contact Sales
                  </Link>
                </div>
              </div>
            </div>
          </div>
        </section>
        <footer className="flex flex-col gap-2 sm:flex-row py-6 w-full shrink-0 items-center px-4 md:px-6 border-t">
          <p className="text-xs text-gray-500 dark:text-gray-400">
            © 2024 Face Emotion Recognition. All rights reserved.
          </p>
          <nav className="sm:ml-auto flex gap-4 sm:gap-6">
            <Link
              className="text-xs hover:underline underline-offset-4"
              href="#"
            >
              Terms of Service
            </Link>
            <Link
              className="text-xs hover:underline underline-offset-4"
              href="#"
            >
              Privacy Policy
            </Link>
          </nav>
        </footer>
      </main>
    </div>
  );
}

function CheckIcon(props: SVGProps<SVGSVGElement>) {
  return (
    <svg
      {...props}
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <polyline points="20 6 9 17 4 12" />
    </svg>
  );
}

function ScanFaceIcon(props: SVGProps<SVGSVGElement>) {
  return (
    <svg
      {...props}
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="M3 7V5a2 2 0 0 1 2-2h2" />
      <path d="M17 3h2a2 2 0 0 1 2 2v2" />
      <path d="M21 17v2a2 2 0 0 1-2 2h-2" />
      <path d="M7 21H5a2 2 0 0 1-2-2v-2" />
      <path d="M8 14s1.5 2 4 2 4-2 4-2" />
      <path d="M9 9h.01" />
      <path d="M15 9h.01" />
    </svg>
  );
}

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <Component />
    </main>
  );
}
