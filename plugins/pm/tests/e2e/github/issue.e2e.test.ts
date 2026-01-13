/**
 * GitHub Issue E2E Tests
 *
 * Tests real GitHub CLI operations without mocks.
 */

import { describe, it, expect, beforeAll, afterAll } from "vitest";
import {
  getRepoInfo,
  isAuthenticated,
  listIssues,
  getIssue,
} from "../../../lib/github.js";
import { GitHubE2EHelper } from "../helpers/github-helper.js";
import { getE2EConfig } from "../config/env.js";

describe("GitHub Issue E2E", () => {
  let helper: GitHubE2EHelper;
  let createdIssueNumber: number;
  const config = getE2EConfig();
  const skipWrite = config.github.skipWrite;

  beforeAll(() => {
    helper = new GitHubE2EHelper();
  });

  afterAll(() => {
    if (!skipWrite) {
      helper.cleanupTestIssues();
    }
  });

  describe("Authentication", () => {
    it("gh CLI is authenticated", () => {
      expect(isAuthenticated()).toBe(true);
    });

    it("can get repo info", () => {
      const info = getRepoInfo();
      expect(info).not.toBeNull();
      expect(info?.owner).toBeDefined();
      expect(info?.repo).toBeDefined();
    });
  });

  describe("Issue CRUD", () => {
    it.skipIf(skipWrite)("creates a new test issue", () => {
      const issue = helper.createTestIssue(
        "Create Issue Test",
        "Testing issue creation via gh CLI"
      );

      expect(issue.number).toBeGreaterThan(0);
      expect(issue.title).toContain("e2e-test-");
      expect(issue.state).toBe("open");

      createdIssueNumber = issue.number;
    });

    it.skipIf(skipWrite)("retrieves created issue via gh CLI", () => {
      const issue = helper.getIssue(createdIssueNumber);

      expect(issue).not.toBeNull();
      expect(issue?.title).toContain("e2e-test-");
      expect(issue?.state).toBe("open");
    });

    it.skipIf(skipWrite)("retrieves issue via lib/github.ts", () => {
      const issue = getIssue(createdIssueNumber);

      expect(issue).not.toBeNull();
      expect(issue?.title).toContain("e2e-test-");
      // gh CLI returns OPEN/CLOSED in uppercase
      expect(issue?.state?.toLowerCase()).toBe("open");
    });

    it.skipIf(skipWrite)("lists issues including test issue", () => {
      const issues = listIssues({ state: "open", limit: 100 });

      const found = issues.find((i) => i.number === createdIssueNumber);
      expect(found).toBeDefined();
    });

    it.skipIf(skipWrite)("adds comment to issue", () => {
      const result = helper.addComment(
        createdIssueNumber,
        "E2E test comment - automated testing"
      );

      expect(result).toBe(true);
    });

    it.skipIf(skipWrite)("closes issue", () => {
      const result = helper.closeIssue(createdIssueNumber, "E2E test complete");
      expect(result).toBe(true);

      const issue = helper.getIssue(createdIssueNumber);
      expect(issue?.state).toBe("closed");
    });

    it.skipIf(skipWrite)("reopens issue", () => {
      const result = helper.reopenIssue(createdIssueNumber);
      expect(result).toBe(true);

      const issue = helper.getIssue(createdIssueNumber);
      expect(issue?.state).toBe("open");
    });
  });

  describe.skipIf(skipWrite)("Issue Listing", () => {
    let listingIssues: number[] = [];

    beforeAll(() => {
      // Create fresh test issues for listing tests
      for (let i = 0; i < 2; i++) {
        const issue = helper.createTestIssue(
          `List Test ${i + 1}`,
          `Testing issue listing #${i + 1}`
        );
        listingIssues.push(issue.number);
      }
    });

    it("lists test issues", () => {
      const issues = helper.listTestIssues("open");

      // Should find at least our newly created issues
      expect(issues.length).toBeGreaterThan(0);

      // All should have the test prefix
      for (const issue of issues) {
        expect(issue.title).toContain("e2e-test-");
      }
    });

    it("lists with state filter", () => {
      const openIssues = helper.listTestIssues("open");

      // All open issues should have state 'open'
      for (const issue of openIssues) {
        expect(issue.state).toBe("open");
      }
    });

    it("respects limit parameter in lib/github.ts", () => {
      const limited = listIssues({ limit: 5 });
      expect(limited.length).toBeLessThanOrEqual(5);
    });
  });
});
